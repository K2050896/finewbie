import numpy as np

def GBM(ntrials,N,time_step,means,cov_mat,S00,an):
    #   ntrials         - number of scenarios
    #   N               - total number of trading periods
    #   means           - mean returns matrix
    #   cov_mat         - covariance matrix
    #   S00             - initial stock price
    #   an              - asset number (1, 2, 3, 4, or 5)
    
    t = np.linspace(0,N,N+1)    # Time in number of months since now

    Sprices = np.matrix(np.zeros((ntrials,N+1)))
    for k in range(ntrials):
        W = np.random.standard_normal(size = N)     # Generating N number of std normal ~ N(0,1)
        W = np.cumsum(W) * np.sqrt(time_step)       # Std Brownian Motion ~ N(0,sqrt(time_step))
        Wt = np.zeros((N+1))                        # Each instance of Wt is only one path; need to generate many
        for i in range(N+1):
            if i == 0:
                Wt[i] = 0                           # To ensure that W(0) = 0
            else:
                Wt[i] = W[i-1]      
        
        for j in range(len(Wt)):
            X0 = (means[an] - 0.5*cov_mat[an,an]) * t[j] + (cov_mat[an,an]**0.5) * Wt[j]
            Sprices[k,j] = S00*np.exp(X0)
    return Sprices
