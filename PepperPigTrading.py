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
def getShareSize():
    return size
#global prevPositions
#prevPositions = np.zeros(100, dtype = "i")

def Strategy(prices):
    #global prevPositions  
    #print(prevPositions)
    myPositions = np.zeros(100, dtype = "i") 
    pairs = [(79, 74), (58, 90), (60,50), (61,36), (62,93), (63,42), (68,59), (69, 3), (70,81), (72, 60), (80, 66), (87, 77), (88, 57), (91, 79), (93, 90), (94, 51)] 
    
    for pair in pairs:
        #stock 74 8.96
        #stock 79 = 6,83
        if (prcAll[0:201, pair[0]] - prcAll[0:201, pair[1]]).mean() > 0:
            #pair[0] is > pair[1]
            stock_expensive = pair[0]
            stock_cheaper = pair[1]
        else:
            #pair[0] is < pair[1]
            stock_expensive = pair[1]
            stock_cheaper = pair[0]

        data_spread = prcAll[0:201, stock_expensive] - prcAll[0:201, stock_cheaper]
        mean_spread = data_spread.mean()
        
        one_std = data_spread.std()
        

        curPrices = prices[-1, :]
        last_price_spread = curPrices[stock_expensive] - curPrices[stock_cheaper]

        #standardize the price spread by subtracting the mean
        last_price_spread_standardized  = last_price_spread - mean_spread
        #Computing max sharesize
        #later it will be getShareSize()
        sharesize_cheaper = 6400 // curPrices[stock_cheaper]
        sharesize_expensive = 6400 // curPrices[stock_expensive]


        if last_price_spread_standardized >= one_std: #short the spread
            #long stock_cheaper
            myPositions[stock_cheaper] = sharesize_cheaper 
            #short stock_expensive
            myPositions[stock_expensive] = -sharesize_expensive

        elif last_price_spread_standardized <= -one_std: #long the spread 
           
            #short stock_cheaper
            myPositions[stock_cheaper] = -sharesize_cheaper            
            #long stock_expensive 
            myPositions[stock_expensive] = sharesize_expensive
        
        elif last_price_spread_standardized <= (one_std/5) and last_price_spread_standardized >=0: #smaller than 1/3 std > 0 
            #if prevPositions[stock_cheaper] != 0 and prevPositions[stock_expensive] != 0: # we have a position
            myPositions[stock_cheaper] = 0
            myPositions[stock_expensive] = 0

        
        elif last_price_spread_standardized >= (-one_std/5) and last_price_spread_standardized <=0: #smaller than 1/3 std > 0 
            #if prevPositions[stock_cheaper] != 0 and prevPositions[stock_expensive] !=0: # we have a position
            myPositions[stock_cheaper] = 0 
            myPositions[stock_expensive] = 0

        else:
            pass
            #do nothing
    #print(myPositions)
    #prevPositions += myPositions
    return myPositions

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
    # check which stock is more expensive than the other
    # short the cheaper one, long the expensive one. 
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    rpos = Strategy(prcSoFar.T)
    currentPos += rpos
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos 
    #[1 , 5 ,0 , 0 ,-5, 0 ,,,,,,............. 100 stocks and the positions we have in them!]
    #[0, 2, 0, 0, +3, 0]
    #[1 , 7 ,0 , 0 ,-2, 0 ,,,,,,............. 100 stocks and the positions we have in them!]








#all stocks from day 151 to day 250
#x = prcAll[0, :]
#z = prcAll[:, 0] #[stock1, stock2, stock3, stock4] Day 1
#so 149 gives the 150th day, so 250 doesnt include 250, so this goes from day 150 to day 251 but doesnt include 251
#it goes up to 250
#y = prcAll[:, 150:250]


# so we have to return our positions based on at the end of the last most pricing day. so eval.py
# gets all the positions at the end of day1, at the end of day2, end of day3 etc... and it will keep calling getmyposition in a loop 
#prcHistSoFar = prcAll[0:202, :]
#newPosOrig = getMyPosition(prcHistSoFar)
#print(newPosOrig)s

#Consider the case where your last position was +30, and the new stock price is $20. 
#If your new position is +100, eval will register this as buying 70 extra shares at $20 a share. If your new position is -200, eval will sell 230 shares also at $20 a share.
#getmyposition returns positions at the end of day (e.g. day before we had [0, 0, 0, 30]) 
#so if we call it again and we wanted to buy 70 more shares, getmyPosition returns [0, 0, 0, 100]