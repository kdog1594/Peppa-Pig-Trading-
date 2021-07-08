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

def getShareSize(beta, stock_cheaper, stock_expensive, current_price):
    #based on spread = stock_expensive - b * stock_cheaper
    expensive_vol = 6250 // current_price[stock_expensive]
    cheaper_value = 6250 * abs(beta)
    #check if cheaper_value > 10000
    #if cheaper_value > 10000:
       # cheaper_value = 10000
    cheaper_vol = cheaper_value // current_price[stock_cheaper]


    return (cheaper_vol, expensive_vol)


def getBetaCoeff(stock_cheaper, stock_expensive):
    stock_cheaper_constant = sm.add_constant(stock_cheaper)
    #results = sm.OLS(stock_expensive, stock_cheaper).fit()
    results = sm.OLS(stock_expensive, stock_cheaper_constant).fit()
    b = results.params[1]
    #b = results.params[0]
    return b
    #spread = stock_expensive - b * stock_cheaper



def Strategy(prices):
    #global prevPositions  
    #print(prevPositions)
    myPositions = np.zeros(100, dtype = "i") 
    pairs = [(2, 11), (2, 30), (2, 45), (2, 55), (2, 66), (2, 96), (2, 99), (9, 36), (11, 9), (11, 12), (11, 13), (11, 37), (11, 45), (11, 97), (12, 9), (12, 11), (12, 18), (12, 76), (18, 12), (18, 20), (19, 35), (19, 58), (19, 61), (20, 18), (20, 48), (23, 14), (29, 5), (30, 22), (30, 45), (30, 51), (30, 59), (30, 64), (30, 68), (30, 76), (30, 97), (31, 38), (35, 19), (36, 45), (38, 20), (38, 31), (38, 43), (38, 48), (39, 16), (41, 49), (44, 11), (44, 13), (44, 30), (44, 36), (44, 59), (44, 62), (44, 64), (44, 68), (44, 76), (44, 77), (44, 97), (45, 2), (45, 9), (45, 13), (45, 30), (45, 36), (45, 64), (45, 68), (45, 77), (45, 97), (46, 11), (46, 12), (46, 45), (46, 50), (46, 52), (46, 53), (46, 54), (46, 55), (46, 56), (46, 57), (46, 60), (46, 61), (46, 62), (46, 64), (46, 65), (46, 66), (46, 68), (46, 69), (46, 70), (46, 72), (46, 73), (46, 77), (46, 79), (46, 81), (46, 84), (46, 87), (46, 89), (46, 92), (46, 93), (46, 94), (46, 96), (48, 20), 
(48, 38), (48, 43), (49, 41), (50, 30), (50, 53), (50, 60), (50, 62), (50, 70), (50, 72), (50, 74), (50, 75), (50, 76), (50, 77), (50, 78), (50, 90), (50, 99), (51, 52), (51, 60), (51, 62), (51, 70), (51, 76), (51, 78), (51, 90), (52, 30), (52, 44), (52, 51), (52, 60), (52, 65), (52, 68), (52, 78), (52, 90), (52, 93), (53, 50), (53, 51), (53, 62), (53, 65), (53, 70), (53, 74), (53, 79), (53, 81), (53, 83), (53, 90), (53, 93), (53, 96), (53, 98), (53, 99), (54, 2), (54, 
27), (54, 46), (54, 55), (54, 56), (54, 57), (54, 58), (54, 79), (54, 83), (54, 84), (54, 88), (54, 89), (54, 92), (54, 94), (54, 98), (55, 2), (55, 19), (55, 44), (55, 46), (55, 54), (55, 56), (55, 57), (55, 58), (55, 67), (55, 68), (55, 69), (55, 70), (55, 73), (55, 74), (55, 79), (55, 81), (55, 84), (55, 85), (55, 87), (55, 88), (55, 91), (55, 92), (55, 94), (55, 95), (55, 96), (55, 98), (56, 19), (56, 27), (56, 46), (56, 54), (56, 55), (56, 57), (56, 61), (56, 69), 
(56, 73), (56, 83), (56, 85), (56, 88), (56, 89), (56, 92), (56, 94), (56, 95), (56, 98), (57, 2), (57, 19), (57, 46), (57, 55), (57, 56), (57, 58), (57, 67), (57, 68), (57, 69), (57, 72), (57, 79), (57, 83), (57, 84), (57, 85), (57, 88), (57, 91), (57, 92), (57, 94), (57, 96), (57, 98), (57, 99), (58, 19), (58, 46), (58, 54), (58, 55), (58, 57), (58, 61), (58, 67), (58, 69), (58, 73), (58, 79), (58, 82), (58, 83), (58, 88), (58, 94), (58, 95), (58, 98), (58, 99), (59, 
30), (59, 36), (59, 44), (59, 76), (60, 44), (60, 50), (60, 51), (60, 52), (60, 62), (60, 64), (60, 68), (60, 74), (60, 75), (60, 76), (60, 77), (60, 79), (60, 81), (60, 87), (60, 90), (61, 19), (61, 27), (61, 46), (61, 54), (61, 56), (61, 57), (61, 58), (61, 69), (61, 73), (61, 88), (61, 89), (61, 91), (61, 92), (61, 94), (61, 95), (61, 98), (62, 45), (62, 50), (62, 51), (62, 53), (62, 60), (62, 64), (62, 65), (62, 70), (62, 76), (62, 79), (62, 86), (62, 90), (62, 93), (63, 51), (63, 52), (63, 65), (63, 68), (63, 70), (63, 72), (63, 76), (63, 79), (63, 93), (64, 30), (64, 44), (64, 45), (64, 46), (64, 52), (64, 60), (64, 62), (64, 68), (64, 70), (64, 76), (64, 77), (64, 79), (64, 87), (64, 90), (64, 96), (65, 51), (65, 52), (65, 53), (65, 62), (65, 63), (65, 70), (65, 74), (65, 76), (65, 77), (65, 78), (65, 90), (66, 2), (66, 19), (66, 34), (66, 46), (66, 68), (67, 63), (67, 71), (67, 72), (67, 79), (67, 82), (67, 83), (67, 85), (67, 88), (67, 99), (68, 30), (68, 44), (68, 45), (68, 46), (68, 50), (68, 51), (68, 52), (68, 55), (68, 60), (68, 64), (68, 70), (68, 72), (68, 76), (68, 77), (68, 78), (68, 82), (68, 88), (68, 90), (68, 93), (68, 97), (69, 2), (69, 19), (69, 27), (69, 46), (69, 54), (69, 55), (69, 56), (69, 57), (69, 58), (69, 72), (69, 84), (69, 88), (69, 91), (69, 92), (69, 94), (69, 96), (69, 98), (69, 99), (70, 50), (70, 51), (70, 53), (70, 62), (70, 63), (70, 64), (70, 65), (70, 68), (70, 72), (70, 74), (70, 76), (70, 81), (70, 90), (70, 96), (70, 99), (71, 2), (71, 46), (71, 53), (71, 70), (71, 79), (71, 99), (72, 2), (72, 24), (72, 44), (72, 45), (72, 46), (72, 50), (72, 57), (72, 63), (72, 67), (72, 68), (72, 70), (72, 71), (72, 76), (72, 77), (72, 78), (72, 79), (72, 83), (72, 87), (72, 91), (72, 93), (72, 96), (72, 98), (72, 99), (73, 19), (73, 54), (73, 55), (73, 56), (73, 57), (73, 58), (73, 61), (73, 69), (73, 84), (73, 88), (73, 89), (73, 
92), (73, 94), (73, 95), (73, 98), (74, 50), (74, 52), (74, 55), (74, 60), (74, 62), (74, 65), (74, 70), (74, 76), (74, 78), (74, 79), (74, 86), (74, 90), (74, 96), (74, 98), (76, 30), (76, 44), (76, 50), (76, 51), (76, 59), (76, 60), (76, 62), (76, 63), (76, 64), (76, 65), (76, 68), (76, 70), (76, 72), (76, 74), (76, 81), (76, 86), (76, 90), (76, 93), (76, 96), (76, 99), (77, 36), (77, 44), (77, 50), (77, 60), (77, 65), (77, 74), (77, 90), (77, 97), (78, 30), (78, 44), (78, 51), (78, 52), (78, 65), (78, 68), (78, 76), (78, 82), (78, 86), (78, 93), (78, 99), (79, 53), (79, 55), (79, 57), (79, 60), (79, 62), (79, 63), (79, 64), (79, 67), (79, 68), (79, 70), (79, 71), (79, 72), (79, 74), (79, 78), (79, 81), (79, 82), (79, 83), (79, 85), (79, 88), (79, 90), (79, 91), (79, 93), (79, 94), (79, 96), (79, 98), (79, 99), (80, 2), (80, 46), (80, 68), (81, 44), (81, 53), (81, 55), (81, 60), (81, 65), (81, 70), (81, 76), (81, 79), (81, 90), (81, 92), (81, 93), (81, 94), (81, 96), (81, 99), (82, 50), (82, 78), (82, 79), (83, 53), (83, 57), (83, 58), (83, 67), (83, 72), (83, 79), (83, 81), (83, 85), (83, 88), (83, 90), (83, 92), (83, 93), (83, 94), (83, 96), (83, 98), (83, 99), (84, 46), (84, 54), (84, 55), (84, 57), (84, 69), (84, 79), (84, 85), (84, 88), (84, 91), (84, 93), (84, 94), (84, 98), (84, 99), (85, 79), (85, 91), (85, 96), (85, 98), (85, 99), (86, 51), (86, 62), (86, 74), (86, 76), (86, 90), (87, 44), (87, 45), (87, 46), (87, 52), (87, 60), (87, 62), (87, 70), (87, 72), (87, 76), (88, 2), (88, 19), (88, 46), (88, 54), (88, 55), (88, 56), (88, 57), (88, 58), (88, 61), (88, 67), (88, 68), (88, 69), (88, 70), (88, 73), (88, 74), (88, 79), (88, 83), (88, 84), (88, 87), (88, 91), (88, 92), (88, 94), (88, 95), (88, 96), (88, 98), (89, 29), (89, 46), (89, 54), (89, 56), (89, 61), (89, 72), (89, 73), (89, 95), (90, 50), (90, 51), (90, 52), (90, 53), (90, 60), (90, 62), (90, 64), (90, 65), (90, 68), (90, 70), (90, 74), (90, 76), (90, 79), (90, 86), (90, 93), (91, 44), (91, 46), (91, 54), (91, 55), (91, 57), (91, 68), (91, 70), (91, 72), (91, 76), (91, 79), (91, 84), (91, 85), (91, 88), (91, 94), (91, 96), 
(91, 98), (91, 99), (92, 27), (92, 46), (92, 54), (92, 55), (92, 56), (92, 57), (92, 68), (92, 69), (92, 73), (92, 79), (92, 83), (92, 85), (92, 88), (92, 89), (92, 91), (92, 95), (92, 98), (93, 2), (93, 11), (93, 44), (93, 46), (93, 52), (93, 53), (93, 62), (93, 63), (93, 68), (93, 72), (93, 76), (93, 77), (93, 78), (93, 79), (93, 81), (93, 83), (93, 84), (93, 87), (93, 90), (93, 96), (94, 2), (94, 19), (94, 46), (94, 54), (94, 55), (94, 56), (94, 57), (94, 58), (94, 69), (94, 79), (94, 81), (94, 83), (94, 84), (94, 88), (94, 91), (94, 98), (94, 99), (95, 19), (95, 27), (95, 46), (95, 54), (95, 55), (95, 56), (95, 57), (95, 58), (95, 61), (95, 66), (95, 69), (95, 73), (95, 84), (95, 88), (95, 89), (95, 91), (95, 92), (95, 94), (95, 98), (96, 2), (96, 19), (96, 27), (96, 46), (96, 53), (96, 55), (96, 64), (96, 68), (96, 70), (96, 72), (96, 74), (96, 76), (96, 77), (96, 78), (96, 79), (96, 81), (96, 82), (96, 83), (96, 88), (96, 89), (96, 91), (96, 93), (96, 98), (97, 11), (97, 30), (97, 36), (97, 44), (97, 45), (97, 50), (97, 52), (97, 77), (97, 93), (98, 2), (98, 12), (98, 19), (98, 46), (98, 53), (98, 54), (98, 55), (98, 56), (98, 57), (98, 58), (98, 68), (98, 69), (98, 72), (98, 79), (98, 83), (98, 84), (98, 85), (98, 87), (98, 88), (98, 91), (98, 92), (98, 94), (98, 95), (98, 96), (98, 99), (99, 30), (99, 50), (99, 53), (99, 57), (99, 58), (99, 67), (99, 69), (99, 70), (99, 71), (99, 72), (99, 76), (99, 78), (99, 79), (99, 81), (99, 82), (99, 83), (99, 85), (99, 90), (99, 91), (99, 94), (99, 98)]
    #[(69,81), (48, 43), (54, 57), (60, 44), (60, 50), (60, 51), (74, 55), (73, 95)]
    #[(79, 74), (58, 90), (60,50), (61,36), (62,93), (68,59), (63,42), (69, 3), (70,81), (72, 60), (80, 66), (87, 77), (88, 57), (91, 79), (93, 90), (94, 51)] 
    
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

        stock_expensive_price = prcAll[0:201, stock_expensive]
        stock_cheaper_price = prcAll[0:201, stock_cheaper]
        b = getBetaCoeff(stock_cheaper_price, stock_expensive_price)
        #data_spread = stock_expensive_price - b * stock_cheaper_price
        data_spread = prcAll[0:201, stock_expensive] - prcAll[0:201, stock_cheaper]
        mean_spread = data_spread.mean()
        
        one_std = data_spread.std()
        

        curPrices = prices[-1, :]
        last_price_spread = curPrices[stock_expensive] - curPrices[stock_cheaper]
        #last_price_spread = curPrices[stock_expensive] - b * curPrices[stock_cheaper]

        #standardize the price spread by subtracting the mean
        last_price_spread_standardized  = last_price_spread - mean_spread
        #Computing max sharesize
        #later it will be getShareSize()
        sharesize_cheaper, sharesize_expensive = getShareSize(b,stock_cheaper, stock_expensive, curPrices)
        #6250 // curPrices[stock_cheaper]
        #sharesize_expensive = 6250 // curPrices[stock_expensive]


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