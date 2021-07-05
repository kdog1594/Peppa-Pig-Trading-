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
    return (df.values).T
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
        if ((prices[pair[0]] - prices[pair[1]]).mean()) > 0:
            #pair[0] is > pair[1]
            stock_expensive = pair[0]
            stock_cheaper = pair[1]
        else:
            #pair[0] is < pair[1]
            stock_expensive = pair[1]
            stock_cheaper = pair[0]

        data_spread = prices[stock_expensive] - prices[stock_cheaper]
        mean_spread = data_spread.mean()
        
        one_std = data_spread.std()

        curPrices = prices[:,-1]
        #print(curPrices)
        last_price_spread = curPrices[stock_expensive] - curPrices[stock_cheaper]
        #print(last_price_spread) # printing the last prices i.e. day 250 
        if last_price_spread >= one_std:
            #short the spread
            return 1
        
        elif last_price_spread <= -one_std:
            #long the spread
            return -1
        
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
        currentPos += rpos
    '''
    #returns [new positions]





def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    currentPos = Strategy(prcSoFar)
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos 
    #[1 , 5 ,0 , 0 ,0, 0 ,,,,,,............. 100 stocks and the positions we have in them!]







prcHistSoFar = prcAll[:,151:250]
#all stocks from day 151 to day 250
x = prcAll[0, :]


# so we have to return our positions based on at the end of the last most pricing day. so eval.py
# gets all the positions at the end of day1, at the end of day2, end of day3 etc... and it will keep calling getmyposition in a loop 
newPosOrig = getMyPosition(prcHistSoFar)
#print(newPosOrig)
#print(prcHistSoFar)
print(x)



    
#prcall[col, row]
#prcall[0, :]
#gives [18.25
#       18.22
#       18.25 
#       ...]
#all prices for stock 0 for 250 days
'''
[ stock1, stock 1, stock,..]
[stock 2, stock 2, stpcl2.//]
'''