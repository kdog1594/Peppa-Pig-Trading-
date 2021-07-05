import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
np.set_printoptions(threshold=sys.maxsize)

def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values)
nInst=100
currentPos = np.zeros(nInst)
pricesFile="./prices250.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

def Strategy(prices):
    #given a last price and given a pair of stocks, --> return a list of tuples [(stock1, position), (stock2, position)]
    mylist = []
    pairs = [(79, 74)] 
    for pair in pairs:
        #stock 74 8.96
        #stock 79 = 6,83
        if (prices[0:150, pair[0]] - prices[0:150, pair[1]]).mean() > 0:
            #pair[0] is > pair[1]
            stock_expensive = pair[0]
            stock_cheaper = pair[1]
        else:
            #pair[0] is < pair[1]
            stock_expensive = pair[1]
            stock_cheaper = pair[0]

        data_spread = prices[0:150, stock_expensive] - prices[0:150, stock_cheaper]
        mean_spread = data_spread.mean()
        
        one_std = data_spread.std()

        curPrices = prices[150, :]
        last_price_spread = curPrices[stock_expensive] - curPrices[stock_cheaper]
        #standardize by subtracting the mean
        last_price_spread = last_price_spread - mean_spread
        # printing the last prices i.e. day 150
        if last_price_spread >= one_std:
            #short the spread
            return 1
        
        elif last_price_spread <= -one_std:
            #long the spread
            return "Long Now"
        
        else:
            #do nothing
            return 0 

    # data = spread -> 79-74 this is the actual spread
    # spread = data - mean.spread() the actual function is data.mean
    # this makes it so that, we look at purely 1STD / 2 STD away from 0 as opposed to 1STD/2STD away from mean
    # one_std = data.std()
    # if spread > one_std:

    #   "short the spread"
    #   check which stock is more expensive than the other
    #   short the more expensive one, and long the cheap one


    # if spread < -one_std:
    # "long the spread"
    #   check which stock is more expensive than the other
    # short the cheaper one, long the expensive one. 
    '''
    for pair in pairs:
        #S74 against S79
        #we will have a list of tuples that spits out what spread to short / long [(1,2), (2,3)]
        #[(5, 50), (10, -20)] = strategy(curPrices, pair)
        #pair is a tuple 
        rpos = np.array([int(x) for x in 1000 * np.random.randn(nins)])
        currentPos += rposs
    #returns [new positions]
    '''




def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    currentPos = Strategy(prcSoFar)
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos 
    #[1 , 5 ,0 , 0 ,0, 0 ,,,,,,............. 100 stocks and the positions we have in them!]








#all stocks from day 151 to day 250
#x = prcAll[0, :]
#z = prcAll[:, 0] #[stock1, stock2, stock3, stock4] Day 1
#so 149 gives the 150th day, so 250 doesnt include 250, so this goes from day 150 to day 251 but doesnt include 251
#it goes up to 250
#y = prcAll[:, 150:250]


# so we have to return our positions based on at the end of the last most pricing day. so eval.py
# gets all the positions at the end of day1, at the end of day2, end of day3 etc... and it will keep calling getmyposition in a loop 
prcHistSoFar = prcAll[0:151, :]
newPosOrig = getMyPosition(prcHistSoFar)
print(newPosOrig)
