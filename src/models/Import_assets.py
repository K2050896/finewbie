import numpy as np
import pandas as pd
#import quandl
from pandas_datareader.data import DataReader
from datetime import datetime as dt

def import_assets(tickers,time_step):

    if time_step == 1:          # Annually
        tf = 'A' 
        nrows = 10 
    elif time_step == 0.5:      # Semi-annually
        tf = '182D'
        nrows = 19
    elif time_step == 1/3:      # Every 4 months
        tf = '122D'
        nrows = 28
    elif time_step == 0.25:     # Quarterly (3 months)
        tf = '91D'
        nrows = 37
    elif time_step == 1/6:      # Every 2 months
        tf = '61D'   
        nrows = 55                     
    elif time_step == 1/12:     # Monthly
        tf = 'M'
        nrows = 109
    elif time_step == 1/52:     # Weekly
        tf = 'W'       
        nrows = 473           
    
    N = len(tickers)
    prices = np.matrix(np.zeros((nrows,N)))         #Preallocate

    today = dt.now()
    today = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    index = 0
    for i in tickers:
        ### Using Yahoo ###
        imported = DataReader(i,'yahoo','2008-11-05',today)                  #Default daily frequency
        imported = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
        prices[:,index] = np.matrix(imported).T
        index = index + 1

    if nrows % 2 == 0:
        breakpoint = int(nrows/2)
        r_prices = prices[0:breakpoint,:]
        bt_prices = prices[breakpoint:nrows,:]
    else:
        breakpoint = int((nrows - 1) / 2)
        r_prices = prices[0:breakpoint,:]
        bt_prices = prices[breakpoint:(nrows-1),:]

    r_returns = np.zeros((r_prices.shape[0]-1,r_prices.shape[1]))
    bt_returns = np.zeros((bt_prices.shape[0]-1,bt_prices.shape[1]))
    for i in range(0,r_returns.shape[0]):
        r_returns[i,:] = (r_prices[i+1,:] - r_prices[i,:])/r_prices[i,:]    #Calculate returns manually
        bt_returns[i,:] = (bt_prices[i+1,:] - bt_prices[i,:])/bt_prices[i,:]

#    for i in range(0,r_returns.shape[0]):
#        df=pd.DataFrame(r_returns[i])
#        df.fillna(0,inplace=True)                                   #Replace NaN with 0's just in case
#        r_returns[i]=df.values
#
#        df=pd.DataFrame(bt_returns[i])
#        df.fillna(0,inplace=True)                                   #Replace NaN with 0's just in case
#        bt_returns[i]=df.values
        
    return r_prices, r_returns, bt_prices, bt_returns;
