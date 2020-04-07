# -*- coding: utf-8 -*-
"""
MSCI 433 Assignment # 1
"""

import pandas as pd
import numpy as np

from pandas_datareader import data
import matplotlib.pyplot as plt


def inputFunction(): 
    start_date= raw_input("Enter the start date:")
    end_date= raw_input("Enter the end date:")
    dates=pd.date_range(start_date, end_date)
    #print dates
    
    k=input("Enter the number of stocks:")
    Stocks=np.empty(k+1, dtype='S8')
    Weights=np.empty(k+1)
    #Prices=np.empty(k)
    
    for i in range(0,k):
        Stocks[i]=raw_input("Enter the name of a stock:")
        Weights[i]=input("Enter the Weight of stock:")
    
    Stocks[k] = 'SPY'
    Weights[k] = 0
    
#    if sum(Weights) > 1:
#        print "Error: Weights sum to more than 1"
#        exit
    
    startValue = input("Portfolio starting value:")
    
    assgn1_main(start_date, end_date, dates, k, Stocks, Weights, startValue)
    
def test_code():
    start_date='2010-01-01'
    end_date='2010-12-31'
    dates=pd.date_range(start_date, end_date)
    k = 5
    Stocks=np.empty(k,dtype='S8')
    Stocks=['GOOG', 'AAPL', 'GLD', 'XOM', 'SPY']
    print Stocks
    Weights=np.empty(k)
    Weights=[0.2, 0.3, 0.4, 0.1, 0]
    startValue=10000

    assgn1_main(start_date, end_date, dates, k, Stocks, Weights, startValue)    
    
    
def assgn1_main(start_date, end_date, dates, k, Stocks, Weights, startValue):
    #Read from the internet
    df1=pd.DataFrame(index=dates)
    
    for s in Stocks:
        dataF = data.DataReader(s, 'yahoo', start_date, end_date)['Adj Close'].rename(s)
        # from https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
        # from https://stackoverflow.com/questions/38133064/get-adj-close-using-pandas-datareader
        
        all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
        dataF = dataF.reindex(all_weekdays)
        dataF = dataF.fillna(method='ffill')
        # from https://www.learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/
        #print dataF
        df1=df1.join(dataF)
        df1=df1.dropna(how='any')
    
        #print df1
    
    #re index the dataframe to simplify below equations
    re_indexedDF = df1.reset_index(drop=True) 
    #print df1     
    #print re_indexedDF
    #Create a dictionary holding stocks and the chosen weights
    stock_Weights = {}
    for i in range(0,len(Stocks)):
        stock_Weights[Stocks[i]]=Weights[i]
    #print "stock_Weights"
    #print stock_Weights
    
    #Find the number of stocks in a portfolio
    stocksInPortfolio = {}
    for stock in re_indexedDF:
        stocksInPortfolio[stock] = int(startValue * stock_Weights[stock] / re_indexedDF.loc[[0], stock])
    #print "stocksInPortfolio"
    #print stocksInPortfolio
    
    #Create Column of daily values of Portfolio
    df1["Portfolio"] = ""
    for i in range(0,len(df1)):
        values = 0
        for k in range(0,len(df1.iloc[0]) - 1):
            values = values + stocksInPortfolio[Stocks[k]]*df1.iloc[i,k]
            # from http://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html
        df1.iloc[i,k+1] = values
    #print "portfolio"
    #print df1['Portfolio']
    
    #find intial value of Portfolio 
    initialValue = df1.iloc[0,len(df1.iloc[0]) - 1]
    #print "initialValue"
    #print initialValue
    
    
    # Output #1
    with pd.ExcelWriter('Portfolio.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Portfolio')
    
    # Output #2 - The visualization of normalized value 
    #of portfolio and SPY (S&P 500 ETF) of the given range.

    Norm=df1/df1.iloc[0]
    df2=pd.DataFrame({"Portfolio":Norm['Portfolio'], "SPY": Norm['SPY']})
    #print "df2"
    #print df2    

    plt.figure();
    df2.plot();
    # from https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
    
    # Output #3 - Average daily return (252 trading days in year)
    Values = df1
    dailyReturn = Values.pct_change(1)
    dailyReturn = dailyReturn.iloc[1:]
    # https://stackoverflow.com/questions/20000726/calculate-daily-returns-with-pandas-dataframe
    
    #print "daily"
    #print dailyReturn
    #print sum(dailyReturn["Portfolio"])
    #print len(dailyReturn["Portfolio"])
    #avgReturn = sum(dailyReturn["Portfolio"])/len(dailyReturn["Portfolio"])
    avgReturn = dailyReturn["Portfolio"].mean()
    
    # Output #4 - Standard deviation of daily returns
    #stdReturn = np.std(dailyReturn["Portfolio"])
    stdReturn = dailyReturn["Portfolio"].std()
    
    # Output #5 - Sharpe ratio of the overall portfolio 
    # (Assume daily risk-free rate is 0)
    # Sharpe Ratio = (return of portfolio)-(Risk-Free rate)/(standatd deviation of portfolio's excess return)
    sharpeRatio = avgReturn / stdReturn
    # Convert Sharpes Ratio to an overall rather than the daily above
    sharpeRatio = sharpeRatio * (252**0.5)
    
    # Output #6 - Ending value of the portfolio 
    endingValue = df1.iloc[len(df1) - 1,len(df1.iloc[0]) - 1]
    #print endingValue
    
    # Output #7 - Cumulative return of the portfolio  
    cumulativeReturn = (endingValue - initialValue) / initialValue
    

    #print df1
    #print Stocks
    #delete the SPY from the stock list
    Stocks =  Stocks[:-1].copy()
    Weights =  Weights[:-1].copy()
        
    print "Start Date: " + start_date
    print "End Date: " + end_date
    print "Symbols: {}".format(Stocks)
    print "Allocations: {}".format(Weights)
    print "Sharpe Ratio: " + str(sharpeRatio)
    print "Volatility (stdev of daily returns): " + str(stdReturn)
    print "Average Daily Return: " + str(avgReturn)
    print "Cumulative Return: " + str(cumulativeReturn)

#test_code()
inputFunction()
