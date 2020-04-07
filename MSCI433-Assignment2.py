# -*- coding: utf-8 -*-
"""
MSCI 433 Assignment # 2

@author: Sami
"""


import pandas as pd
import numpy as np
#from pandas_datareader import data
import matplotlib.pyplot as plt
import scipy.optimize as sop



def inputFunction():
    #INPUT
    startValue = input("Portfolio starting value:")
    start_date= raw_input("Enter the start date:")
    end_date= raw_input("Enter the end date:")
    #k=input("Enter the number of stocks:")
    Stocks=np.empty(k, dtype='S8')
    for i in range(0,k):
        Stocks[i]=raw_input("Enter the name of a stock:")
    k=len(Stocks)
    gen_plot=input("Generate a plot of data? (True/False):")
    startValue=raw_input("What is the starting value of the portfolio:")
    optimize_portfolio(start_date, end_date, k, Stocks, gen_plot);

def test_code1():
    start_date='2012-01-01'
    end_date='2013-12-31'
    Stocks=['AAPL','GLD','XOM','GOOG']
    k=len(Stocks)
    gen_plot=True
    startValue=10000
    optimize_portfolio(start_date, end_date, k, Stocks, gen_plot);

def test_code2():
    start_date='2012-01-01'
    end_date='2013-12-31'
    long_stocks=['AAPL','GLD','XOM','GOOG']
    short_stocks=['IBM','NFLX']
    k=len(long_stocks+short_stocks)
    gen_plot=True
    startValue=10000
    optimize_portfolio_shortlong(start_date, end_date, k, long_stocks, short_stocks, gen_plot)

def Const1(x,k):  
    y=0
    for i in x:
        y = y + x[i]
    return y-1 #use an array for x??
    
def optimize_portfolio(start_date, end_date, k, Stocks, gen_plot):
    # Optimize for maximum Sharpe Ratio
    dates=pd.date_range(start_date, end_date)
    
    df1=pd.DataFrame(index=dates)
    
    for s in Stocks:
        data = pd.read_csv("{}.csv".format(s),usecols=['Date', 'Adj Close'],index_col='Date')
        data = data.rename(columns={'Adj Close': "{}".format(s)})
        df1=df1.join(data)
        df1=df1.dropna()
    
    Return=np.zeros((df1.shape[0],len(Stocks)))
    #Stat=pd.DataFrame(index=Stocks)
    Ave=np.zeros(len(Stocks))
    Std=np.zeros(len(Stocks))
    Var=np.zeros(len(Stocks))
    COV=np.zeros((len(Stocks),len(Stocks)))
    d=df1.index       
    for i in range(0,df1.shape[0]):
        for j in range (0,len(Stocks)):
            Return[i][j]=df1.loc[d[i],Stocks[j]]/df1.loc[d[i-1],Stocks[j]]-1
        
    for i in range(0,len(Stocks)):
        Ave[i]=Return[:,i].mean()
        Std[i]=Return[:,i].std()
        Var[i]=Return[:,i].var()
    
    #FUNCTION
    x0=[]
    for num in range(0,k):
        x0[num]=1/k
    b=()
    for spot in range(0,k):
        b.append((0,1))
        
    const={'type':'eq','fun':Const1}
    sol =sop.minimize (Sharpe, x0, method='SLSQP', bounds=b, constraints=const, options={'disp':True})
    
    print "Solution"
    print sol
    
    #OUTPUT
    print "Allocations"
    print Weights
    print "Culumative Return"
    print cumulative_return
    print "Average Daily Return"
    print average_return_daily
    print "Daily Standard Deviation"
    print Std_dev_daily
    print "Sharpe Ratio"
    print Sharpe_ratio
    
    if gen_plot=="True":
        plt.figure;
        average_return_daily.plot();
        plt.savefig('comparision.png')
    
    
    
def optimize_portfolio_shortlong():
    x=[i]
    #hello
    #short selling should be greater than -1
    
def Sharpe (x): #From Quiz 2_answer
    #Calculating portfolio Variance
    P_Variance = 0
    
    for i in range(0,len(Stocks)):
        P_Variance += P_Variance + x[i]**2*Var[i]
        
    for i in range(0,len(Stocks)):
        for j in range(i+1,len(Stocks)):
            P_Variance = P_Variance+2*(x[i]*x[j]*COV[i,j])
    #calculating portfolio average return
    P_Return=0
    for i in range(0,len(Stocks)):
        P_Return = P_Return + (x[i]*Ave[i])
    
    Sharpe=(P_Return-0)/np.sqrt(P_Variance)
    return -Sharpe

    
test_code1()
    
    
    
    