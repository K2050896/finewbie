import numpy as np
import pandas as pd
#import quandl
from pandas_datareader.data import DataReader
import datetime as dt

def import_assets(Y,T,tickers,time_step):
    #   Y           - original length of gaol in years (always constant)
    #   T           - remaining length of goal in years
    #   Y - T       - will give me how much time has passed in years

    if time_step == 1:          # Annually
        tf = 'A' 
    elif time_step == 0.5:      # Semi-annually
        tf = '182D'
    elif time_step == 1/3:      # Every 4 months
        tf = '122D'
    elif time_step == 0.25:     # Quarterly (3 months)
        tf = '91D'
    elif time_step == 1/6:      # Every 2 months
        tf = '61D'                      
    elif time_step == 1/12:     # Monthly
        tf = 'M'
    elif time_step == 1/52:     # Weekly
        tf = 'W'               
    

    date_now = dt.datetime.now()
    date_now = date_now + dt.timedelta(days=int((Y-T)*365.25))
    fake_today = str(date_now.year-3) + '-' + str(date_now.month) + '-' + str(date_now.day)

    ### Using Yahoo ###
    imported = DataReader(tickers[0],'yahoo','2008-11-05',fake_today)           #Default daily frequency
    imported0 = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
    
    imported = DataReader(tickers[1],'yahoo','2008-11-05',fake_today)           #Default daily frequency
    imported1 = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
    
    imported = DataReader(tickers[2],'yahoo','2008-11-05',fake_today)           #Default daily frequency
    imported2 = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
    
    imported = DataReader(tickers[3],'yahoo','2008-11-05',fake_today)           #Default daily frequency
    imported3 = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
    
    imported = DataReader(tickers[4],'yahoo','2008-11-05',fake_today)           #Default daily frequency
    imported4 = imported.groupby(pd.TimeGrouper(freq=tf))['Close'].mean()   #For yearly frequency
    
    

    prices0 = np.matrix(imported0).T
    prices1 = np.matrix(imported1).T
    prices2 = np.matrix(imported2).T
    prices3 = np.matrix(imported3).T
    prices4 = np.matrix(imported4).T

    prices = np.concatenate((prices0,prices1,prices2,prices3,prices4),axis=1)

    returns = np.zeros((prices.shape[0]-1,prices.shape[1]))
    for i in range(0,returns.shape[0]):
        returns[i,:] = (prices[i+1,:] - prices[i,:])/prices[i,:]

    return prices, returns
