# import matplotlib.pyplot as plt
import numpy as np
# from time import clock
from src.models.portfolios.Import_assets import import_assets as ia
from src.models.portfolios.SP import stochastic_programming as sp
from src.models.portfolios.GBM import GBM
from src.models.portfolios.portfolio import Portfolio
from src.models.profiles.profile import Profile
import src.models.portfolios.constants

def port_opt(constants, port_id):
    
    # Grab profile and portfolio objects
    prof = Profile.from_mongo(port_id)
    port = Portfolio.from_mongo(port_id)
    
    # Function for converting any rate to the specified time step
    def int_rate_convert(annual_int_rate,time_step):
        eff_rate = (1 + annual_int_rate)**(time_step) - 1
        return eff_rate
    
    tickers = constants.TICKERS
    mgmt_fees = constants.MGMT_FEES     # annual management fees
    trans_costs = constants.TRANS_COSTS # transaction costs
    
    Y = prof['horizon'][-1]                     # Entire length of planning horizon (WEBAPP INPUT)
    T = max(prof['time_left'],0)                # Number of years left (WEBAPP INPUT)
    
    if Y < 2:
        time_step = 1/12        # Trading frequency is monthly
    elif 2 <= Y <= 5:
        time_step = 1/4         # Trading frequency is quarterly
    elif 5 < Y <= 10:
        time_step = 1/2         # Trading frequency is semi-annually
    elif Y > 10:
        time_step = 1           # Trading frequency is annually
    
    N = int(T / time_step) + 1  # Total number of trading periods
    
    # Convert the annual rate to any frequency
    annual_int_rate = constants.INT_RATE      # assume constant interest rate for cash investment
    eff_rate = int_rate_convert(annual_int_rate,time_step)
    
    # Convert management fees to one-time expenses at the end of the planning horizon
    eff_fees = np.zeros((len(mgmt_fees)+1,1))
    for m in range(0,len(mgmt_fees)):
        eff_fees[m] = int_rate_convert(mgmt_fees[m],N * time_step)
    eff_fees[m+1] = 0           # assume mgmt fees of cash investment is 0
                                                
    # Prices and returns of assets; nrows x nassets
    prices = None
    while prices is None:
        try:
            prices, returns = ia(Y,T,tickers,time_step)     
        except:
            pass
    means = np.mean(returns.T,axis=1)                    # mean return vector; nassets x 1
    cov_mat = np.cov(returns.T)                          # covariance matrix; nassets x nassets
    
    # Terminate when time left = 0
    if T == 0:
        temp = port['shares1'][-1]
        shares = np.matrix(np.zeros((6,1)))
        for i in range(0,len(shares)):
            shares[i] = float(temp[i])
            
        # the variable shares is a result from last optimization
        net_val = np.matrix(np.zeros((len(shares),1)))
        for i in range(0,len(shares)-1):
            net_val[i] = shares[i] * prices[-1,i]
        net_val[i+1] = shares[i+1]              # This is the 'true' net wealth
        init_con = float(np.sum(net_val))       # Terminal portfolio value!
        init_alloc = []
        nassets = 6
        for i in range(0,nassets):
            init_alloc.append(float(net_val[i] / init_con)) # Terminal asset allocation!
        
        inflation = constants.INFLATION
        goal = prof['goal'] * (1 + inflation)**Y
        reached = round(init_con / goal,3)
                                    
        port["reached"].append(reached)
        port["alloc_percent"].append(init_alloc)
        Portfolio.update_portfolio(port['port_id'],{"port_id": port['port_id'],"user_email":port['user_email'],"name":prof['name'],"mean_term_wealth": port["mean_term_wealth"],
                                                    "mean_var_wealth": port["mean_var_wealth"],"alloc_percent": port["alloc_percent"],"shares0": port["shares0"],
                                                    "shares1": port["shares1"],"cont": port["cont"],"reached": port["reached"],"ambitious": port["ambitious"]})
        return None

    # Simulate stock prices for each asset; each is ntrials x len(Wt)
    S00 = prices[-1,0]  # Initial stock price for asset 1
    S01 = prices[-1,1]  # Initial stock price for asset 2
    S02 = prices[-1,2]  # Initial stock price for asset 3
    S03 = prices[-1,3]  # Initial stock price for asset 4
    S04 = prices[-1,4]  # Initial stock price for asset 5
    
    ntrials = 10
    # start_time = clock()
    Sprices0 = GBM(ntrials,N,time_step,means,cov_mat,S00,0)
    Sprices1 = GBM(ntrials,N,time_step,means,cov_mat,S01,1)
    Sprices2 = GBM(ntrials,N,time_step,means,cov_mat,S02,2)
    Sprices3 = GBM(ntrials,N,time_step,means,cov_mat,S03,3)
    Sprices4 = GBM(ntrials,N,time_step,means,cov_mat,S04,4)
    # print("--- %s seconds ---" % (clock() - start_time))
    Sprices = np.concatenate((np.mean(Sprices0,axis=0),np.mean(Sprices1,axis=0),np.mean(Sprices2,axis=0),np.mean(Sprices3,axis=0),np.mean(Sprices4,axis=0)))
    
    # Calculate returns from the simulated stock prices of each asset
    Sreturns0 = np.matrix(np.zeros((ntrials,N)))
    Sreturns1 = np.matrix(np.zeros((ntrials,N)))
    Sreturns2 = np.matrix(np.zeros((ntrials,N)))
    Sreturns3 = np.matrix(np.zeros((ntrials,N)))
    Sreturns4 = np.matrix(np.zeros((ntrials,N)))
    for k in range(N):
        Sreturns0[:,k] = (Sprices0[:,k+1] - Sprices0[:,k]) / Sprices0[:,k]
        Sreturns1[:,k] = (Sprices1[:,k+1] - Sprices1[:,k]) / Sprices1[:,k]
        Sreturns2[:,k] = (Sprices2[:,k+1] - Sprices2[:,k]) / Sprices2[:,k]
        Sreturns3[:,k] = (Sprices3[:,k+1] - Sprices3[:,k]) / Sprices3[:,k]
        Sreturns4[:,k] = (Sprices4[:,k+1] - Sprices4[:,k]) / Sprices4[:,k]
    
    # Account for coupon rates as part of the bond ETFs' returns
    cr3 = constants.COUPONS[0]     # CSJ average coupon rate is about 1.6%
    cr4 = constants.COUPONS[1]     # BLV average coupon rate is about 4.5%
    Sreturns3 = Sreturns3 + int_rate_convert(cr3,time_step)       
    Sreturns4 = Sreturns4 + int_rate_convert(cr4,time_step)
    
    # Cash investment i.e. savings account with constant interest rate
    Sreturns5 = np.ones((Sreturns0.shape[0],Sreturns0.shape[1])) * eff_rate
    
    ## Example plot of simulated asset returns
    #plt.plot(Sreturns0.T,alpha=0.5)
    #plt.show()
    
    # Calculate and reorganize total returns matrix
    # Notes on the matrix Returns
    # This is the total return matrix. For example, for 2 assets and 2 scenarios:
    # Row 1: asset 1 under scenario 1
    # Row 2: asset 2 under scenario 1
    # Row 3: asset 1 under scenario 2
    # Row 4: asset 2 under scenario 2
    nassets = len(tickers) + 1
    temp = 1 + np.concatenate((Sreturns0,Sreturns1,Sreturns2,Sreturns3,Sreturns4,Sreturns5))     # total returns  
    Returns = np.matrix(np.zeros((temp.shape[0],temp.shape[1])))
    for i in range(0,ntrials):
        for j in range(0,nassets):
            Returns[j+i*nassets,:] = temp[i+j*ntrials,:]
    
    ### Solve the problem!
    lamb = prof['lamb']
    if lamb == 0:
        lamb = 0
    elif lamb == 0.25:
        lamb = 0.01
    elif lamb == 0.5:
        lamb = 0.05
    elif lamb == 0.75:
        lamb = 0.4
    elif lamb == 1:
        lamb = 0.99
    dis_inc = prof['dis_inc'][-1] * 12 * time_step   # Investor's disposable income within a single trading period
    if Y - T == 0:
        init_con = prof['init_con']              # intial contribution to goal (User input)
        init_alloc = prof['init_alloc']          # Recommended initial alloc (WEBAPP INPUT)
    else:
        temp = port['shares1'][-1]
        shares = np.matrix(np.zeros((6,1)))
        for i in range(0,len(shares)):
            shares[i] = float(temp[i])
        # the variable shares is a result from last optimization
        net_val = np.matrix(np.zeros((len(shares),1)))
        for i in range(0,len(shares)-1):
            net_val[i] = shares[i] * prices[-1,i]
        net_val[i+1] = shares[i+1]              # This is the 'true' net wealth
        init_con = float(np.sum(net_val))
        init_alloc = []
        for i in range(0,nassets):
            init_alloc.append(float(net_val[i] / init_con)) # New allocation restriction at "t = 0"
    
    # Financial goal (target) accounted for inflation (assumed to be constant at 2% annual)
    inflation = constants.INFLATION
    goal = prof['goal'] * (1 + int_rate_convert(inflation,time_step))**((Y-T)/time_step)
    
    # Optimize!
    # start_time = clock()   
    opt_soln, P, q = sp(nassets, ntrials, Y, N, lamb, dis_inc, Returns, init_con, goal, eff_fees, init_alloc)
    # print("--- %s seconds ---" % (clock() - start_time))     # Measure run time
    
    dv = np.matrix(opt_soln['x'])
    mean_term_wealth = round(float(q.T * dv),2)         # Mean of terminal wealths
    mean_var_wealth = round(float(dv.T * P * dv)**0.5,2)     # Variance of wealths
    
    # Determine if the goal is "ambitious"
    diff = goal - mean_term_wealth
    ambitious = 0
    if diff > 0:
        ambitious = 1
        
    # If the goal is ambitious, how much extra should the investor be contributing to meet the goal (monthly)?
    if ambitious == 1 and (N - 1) != 0:
        extra_dis_inc = (diff / (N - 1)) / (12 * time_step)
        extra_time = diff/mean_term_wealth * T   
    else:
        extra_dis_inc = 0
        extra_time = 0
    
    importance = prof['importance']
    if importance == 1:
        extra_dis_inc = 0
    elif importance == 2:
        extra_dis_inc = 0.25 * extra_dis_inc
        extra_time = 0.75 * extra_time
    elif importance == 3:
        extra_dis_inc = 0.5 * extra_dis_inc
        extra_time = 0.5 * extra_time
    elif importance == 4:
        extra_dis_inc = 0.75 * extra_dis_inc
        extra_time = 0.25 * extra_time
    else:
        extra_time = 0
    
    # t = 0 # of shares
    shares0 = dv[0:6]
    shares0[0:-1] = shares0[0:-1] / Sprices[:,0]

    # t = 1 average asset allocation across all scenarios 
    # (need this for next optimization)
    if N > 1:
        collect = np.matrix(np.zeros((nassets,ntrials)))
        ctr = 0
        for s in range(0,ntrials):
            ctr = ctr + (nassets + 1)
            collect[:,s] = dv[ctr:ctr + nassets]
        avg_alloc = np.mean(collect,axis=1) 
        alloc_percent = avg_alloc / np.sum(avg_alloc)
        shares1 = avg_alloc
        shares1[0:-1] = avg_alloc[0:-1] / Sprices[:,1] # Cash investment is left in units of $
        for i in range(0,nassets-1):
            shares1[i] = shares1[i] * (1 - trans_costs[i]) # take away transaction costs
    
        # Additional contribution required by next time step
        cont = round(float(dv[nassets:nassets+1]),2)
    else:
        collect = np.matrix(np.zeros((nassets,ntrials)))
        ctr = 0
        for s in range(0,ntrials):
            ctr = ctr + nassets
            collect[:,s] = dv[ctr:ctr + nassets]
        avg_alloc = np.mean(collect,axis=1) 
        alloc_percent = avg_alloc / np.sum(avg_alloc)
        shares1 = avg_alloc
        shares1[0:-1] = avg_alloc[0:-1] / Sprices[:,1] # Cash investment is left in units of $
        for i in range(0,nassets-1):
            shares1[i] = shares1[i] * (1 - trans_costs[i]) # take away transaction costs

        # Additional contribution required by next time step
        cont = 0 # Since there will no next time period
    
    # % reached of financial goal target
    reached = round(float(init_con / goal),3)
    reached_dollar = round(reached * goal,2) # In dollar value
    
    # Time weighted rate of return (TWRR)
    if Y - T == 0:
        hprr = 0
        twrr = 0
    if Y - T != 0:
        # holding period return i.e. rate of return on the portfolio in a single time period
        hprr = round((reached - port['reached'][-1]) / port['reached'][-1] - port['cont'][-1]/(goal*port['reached'][-1]),3)
        twrr = round((1 + port['twrr'][-1]) * (1 + hprr) - 1,3)
    
    # Add elements into lists for historical view
    prof["horizon"].append((prof["horizon"][-1] + extra_time))
    prof["dis_inc"].append((prof["dis_inc"][-1] + extra_dis_inc))
    
    # Update profile by changing the length of time remaining
    Profile.update_profile(prof['port_id'],{"port_id": prof['port_id'],"user_email": prof['user_email'],"name":prof['name'],
                                            "goal":prof['goal'],"horizon": prof['horizon'], "time_left": prof['time_left'] - time_step + extra_time,
                                            "init_con":prof['init_con'],"dis_inc": prof['dis_inc'],"init_alloc": init_alloc,
                                            "lamb": prof['lamb'],"importance": prof['importance']})
    
    # Update portfolio (export)
    shares0_ = []
    shares1_ = []
    alloc_percent_ = []
    for i in range(0,nassets):
        shares0_.append(float(shares0[i]))
        shares1_.append(float(shares1[i]))
        alloc_percent_.append(float(alloc_percent[i]))
        
    
    # Add elements into lists for historical view
    port["mean_term_wealth"].append(mean_term_wealth)
    port["mean_var_wealth"].append(mean_var_wealth)
    port["alloc_percent"].append(alloc_percent_)
    port["shares0"].append(shares0_)
    port["shares1"].append(shares1_)
    port["cont"].append(cont)
    port["reached"].append(reached)
    port["reached_dollar"].append(reached_dollar)
    port["hprr"].append(hprr)
    port["twrr"].append(twrr)
    port["ambitious"].append(ambitious)
    Portfolio.update_portfolio(port['port_id'],{"port_id": port['port_id'],"user_email":port['user_email'],"name":prof['name'],"mean_term_wealth": port["mean_term_wealth"],
                                                "mean_var_wealth": port["mean_var_wealth"],"alloc_percent": port["alloc_percent"],"shares0": port["shares0"],
                                                "shares1": port["shares1"],"cont": port["cont"],"reached": port["reached"],"reached_dollar":port["reached_dollar"],"hprr":port["hprr"],"twrr":port["twrr"],"ambitious": port["ambitious"]})

#    # Pie Chart: Terminal average asset allocation across all scenarios
#    temp = dv[dv.shape[0]-nassets*ntrials:dv.shape[0]]
#    term_wealths = np.zeros((nassets,ntrials))
#    for s in range(0,ntrials):
#        for a in range(0,nassets):
#            term_wealths[a,s] = temp[a + s*nassets]
#    taaa = np.mean(term_wealths,axis=1)
#    plt.pie(taaa,labels=['SPY','IWM','VEU','CSJ','BLV','Cash Investment'],autopct='%1.1f%%')
    
    ## Optimize for different values of lamb
#    lamb = np.linspace(0,1,70)
#    mean_wealths = []
#    var_wealths = []
#    obj = []
#    for l in lamb[0:len(lamb)-1]:
#        opt_soln, P, q = sp(nassets, ntrials, Y, N, l, dis_inc, Returns, init_con, goal, eff_fees, init_alloc)
#        dv = np.matrix(opt_soln['x'])
#        mean_wealth = float(q.T * dv)
#        var_wealth = float(dv.T * P * dv)
#        mean_wealths.append(mean_wealth)
#        var_wealths.append(var_wealth)
#        obj.append(l*var_wealth - (1- l)*mean_wealth)
#    plt.plot(lamb[0:len(lamb)-1],obj) # Efficient frontier for mean-variance tradeoff
    
#    # Average cash contribution
#    ctr = nassets
#    contr = []
#    for i in range(0,ntrials*(N-1)):
#        contr.append(dv[ctr:ctr+1])
#        ctr = ctr + nassets + 1
#    np.mean(contr)
    
#    return mean_term_wealth, mean_var_wealth,alloc_percent,shares0,shares1,cont,reached,ambitious
    return None
