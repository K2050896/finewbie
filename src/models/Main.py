import matplotlib.pyplot as plt
import numpy as np
from time import clock
from Import_assets import import_assets as ia  
from SP import stochastic_programming as sp
from GBM import GBM

tickers = ['SPY','IWM','VEU','CSJ','BLV']
mgmt_fees = [0.000945,0.002,0.0011,0.002,0.0007]     # annual management fees

Y = 3                       # Original number of years (CONSTANT) (WEBAPP INPUT)
T = 3                       # Number of years left (WEBAPP INPUT)
if Y < 2:
    time_step = 1/12        # Trading frequency is monthly
elif 2 <= Y <= 5:
    time_step = 1/4         # Trading frequency is quarterly
elif 5 < Y <= 10:
    time_step = 1/2         # Trading frequency is semi-annually
elif Y > 10:
    time_step = 1           # Trading frequency is annually

N = int(T / time_step)      # Total number of trading periods

# Convert the annual rate to any frequency
annual_int_rate = 0.01      # assume constant interest rate for cash investment
def int_rate_convert(annual_int_rate,time_step):
    eff_rate = (1 + annual_int_rate)**(time_step) - 1
    return eff_rate
eff_rate = int_rate_convert(annual_int_rate,time_step)

# Convert management fees to one-time expenses at the end of the planning horizon
eff_fees = np.zeros((len(mgmt_fees)+1,1))
for m in range(0,len(mgmt_fees)):
    eff_fees[m] = int_rate_convert(mgmt_fees[m],N * time_step)
eff_fees[m+1] = 0           # assume mgmt fees of cash investment is 0
                                            
# Prices and returns of assets; nrows x nassets
prices, returns = ia(Y,T,tickers,time_step)     
means = np.mean(returns.T,axis=1)                    # mean return vector; nassets x 1
cov_mat = np.cov(returns.T)                          # covariance matrix; nassets x nassets

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

## Example plot of simulated asset prices
#plt.plot(Sprices0.T,alpha=0.5)
#plt.show()

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
cr3 = 0.016         # CSJ average coupon rate is about 1.6%
cr4 = 0.045         # BLV average coupon rate is about 4.5%
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
lamb = 0.016                           # User input risk aversion factor
                                       # Recommend using: 0, 0.008, 0.012, 0.016, 0.02
dis_inc = 500                          # comfortable disposable income given the trading period
if Y - T == 0:
    init_con = 7000                    # intial contribution to goal (User input)
    init_alloc = [0.15,0.15,0.1,0.05,0.05,0.5] # Recommended initial alloc (WEBAPP INPUT)
#else:
#    # the variable shares is a result from last optimization
#    net_val = np.matrix(np.zeros((len(shares),1)))
#    for i in range(0,len(shares)-1):
#        net_val[i] = shares[i] * prices[-1,i]
#    net_val[i+1] = shares[i+1]              # This is the 'true' net wealth
#    init_con = np.sum(net_val)
#    init_alloc = list(net_val / init_con)   # New allocation restriction at "t = 0"

# Financial goal (target) accounted for inflation (constant 2%)
goal = 10000 * (1 + int_rate_convert(0.02,time_step))**(Y-T) 

# Optimize!
# start_time = clock()   
opt_soln, P, q = sp(nassets, ntrials, Y, N, lamb, dis_inc, Returns, init_con, goal, eff_fees, init_alloc)
# print("--- %s seconds ---" % (clock() - start_time))     # Measure run time

dv = np.matrix(opt_soln['x'])
mean_term_wealth = round(float(q.T * dv),2)         # Mean of terminal wealths
mean_var_wealth = round(float(dv.T * P * dv),2)     # Variance of wealths

# Determine if the goal is "ambitious"
diff = goal - mean_term_wealth
if diff > 0:
    ambitious = 1

# t = 1 average asset allocation across all scenarios (need this for next optimization)
collect = np.matrix(np.zeros((nassets,ntrials)))
ctr = 0
for s in range(0,ntrials):
    ctr = ctr + (nassets + 1)
    collect[:,s] = dv[ctr:ctr + nassets]
avg_alloc = np.mean(collect,axis=1) 
alloc_percent = avg_alloc / np.sum(avg_alloc)
shares = avg_alloc
shares[0:-1] = avg_alloc[0:-1] / prices[-1,:].T # Cash investment is left in units of $

# Additional contribution required by next time step
cont = round(float(dv[nassets:nassets+1]),2)

# % reached of financial goal target
reached = round(float(init_con / goal),3)

## Pie Chart: Terminal average asset allocation across all scenarios
#temp = dv[dv.shape[0]-nassets*ntrials:dv.shape[0]]
#term_wealths = np.zeros((nassets,ntrials))
#for s in range(0,ntrials):
#    for a in range(0,nassets):
#        term_wealths[a,s] = temp[a + s*nassets]
#taaa = np.mean(term_wealths,axis=1)
#plt.pie(taaa,labels=['SPY','IWM','VEU','CSJ','BLV','Cash Investment'],autopct='%1.1f%%')

#### Optimize for different values of lamb and plot changes in mean and variance
#lamb = np.linspace(0,0.1,11)
#mean_wealths = []
#var_wealths = []
#for l in lamb[0:len(lamb)-1]:
#    opt_soln, P, q = sp(nassets, ntrials, Y, N, l, dis_inc, Returns, init_con, goal, eff_fees, init_alloc)
#    dv = np.matrix(opt_soln['x'])
#    mean_wealth = float(q.T * dv)
#    var_wealth = float(dv.T * P * dv)
#    mean_wealths.append(mean_wealth)
#    var_wealths.append(var_wealth)
#plt.plot(lamb[0:len(lamb)-1],mean_wealths)
#plt.plot(lamb[0:len(lamb)-1],var_wealths)
