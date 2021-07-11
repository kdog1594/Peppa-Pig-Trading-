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
    #cheaper_value = 6250 * abs(beta)
    #check if cheaper_value > 10000
    #if cheaper_value > 10000:
       # cheaper_value = 10000
    cheaper_vol = expensive_vol * abs(beta)
    #cheaper_vol = cheaper_value // current_price[stock_cheaper]


    return (cheaper_vol, expensive_vol)


def getBetaCoeff(stock_cheaper, stock_expensive):
    stock_cheaper_constant = sm.add_constant(stock_cheaper, has_constant='add')
    #print(stock_cheaper_constant)
    #results = sm.QuantReg(stock_expensive, stock_cheaper).fit()
    #results = sm.GLSAR(stock_expensive, stock_cheaper).fit()
    #results = sm.OLS(stock_expensive, stock_cheaper_constant).fit()
    results = sm.OLS(stock_expensive, stock_cheaper_constant).fit()
    #print(results.params)
    b = results.params[1]
    theo_spread = results.params[0]
    return (b, theo_spread)
    #spread = stock_expensive - b * stock_cheaper

def Strategy(prices):
    myPositions = np.zeros(100, dtype = "i")      
    pairs = [(11, 37), (19, 35), (30, 51), (30, 76), (44, 59), (44, 97), (45, 13), (45, 68), (45, 97), (46, 61), (46, 72), (46, 96), (48, 20), (48, 38), (50, 53), (50, 60), (50, 62), (50, 70), (50, 72), (50, 76), (50, 78), (50, 90), (51, 52), (51, 60), (51, 62), (51, 70), (51, 76), (51, 90), (52, 51), (52, 60), (52, 65), (52, 90), (52, 93), (53, 50), (53, 62), (53, 65), (53, 70), (53, 74), (53, 79), (53, 81), (53, 90), (53, 93), (53, 98), (53, 99), (54, 27), (54, 56), (54, 58), (54, 88), (54, 89), (54, 98), (55, 54), (55, 56), (55, 57), (55, 58), (55, 68), (55, 69), (55, 74), (55, 79), (55, 81), (55, 84), (55, 88), (55, 91), (55, 92), (55, 94), (55, 95), (55, 96), (55, 98), (56, 54), (56, 55), (56, 57), (56, 61), (56, 69), (56, 73), (56, 83), (56, 88), (56, 89), (56, 92), (56, 94), (56, 98), (57, 55), (57, 58), (57, 69), (57, 72), (57, 79), (57, 83), (57, 84), (57, 85), (57, 88), (57, 91), (57, 92), (57, 94), (57, 98), (57, 99), (58, 54), (58, 55), (58, 57), (58, 69), (58, 83), (58, 88), (58, 94), (58, 95), (58, 98), (58, 99), (60, 50), (60, 51), (60, 52), (60, 62), (60, 64), (60, 68), (60, 74), (60, 76), (60, 77), (60, 79), (60, 81), (60, 90), (61, 46), (61, 56), (61, 58), (61, 73), (61, 88), (61, 89), (61, 91), (61, 92), (61, 95), (62, 50), (62, 51), (62, 53), (62, 60), (62, 64), (62, 65), (62, 70), (62, 76), (62, 79), (62, 86), (62, 93), (63, 65), (63, 70), (63, 72), (63, 76), (63, 79), (63, 93), (64, 44), (64, 52), (64, 60), (64, 62), (64, 68), (64, 70), (64, 76), (64, 79), (64, 87), (64, 90), (64, 96), (65, 52), (65, 53), (65, 62), (65, 63), (65, 70), (65, 74), (65, 76), (65, 77), (65, 78), (67, 72), (67, 79), (67, 82), (67, 99), (68, 44), (68, 45), (68, 52), (68, 55), (68, 60), (68, 64), (68, 70), (68, 72), (68, 76), (68, 77), (68, 90), (69, 2), (69, 55), (69, 57), (69, 58), (69, 84), (69, 88), 
    (69, 92), (69, 94), (69, 96), (69, 98), (69, 99), (70, 50), (70, 51), (70, 53), (70, 62), (70, 64), (70, 65), (70, 68), (70, 72), (70, 74), 
    (70, 76), (70, 81), (70, 90), (70, 96), (70, 99), (71, 53), (71, 70), (71, 79), (72, 46), (72, 50), (72, 63), (72, 67), (72, 68), (72, 70), 
    (72, 76), (72, 79), (72, 83), (72, 91), (72, 93), (72, 96), (72, 98), (72, 99), (73, 55), (73, 56), (73, 61), (73, 92), (74, 50), (74, 52), 
    (74, 55), (74, 60), (74, 65), (74, 70), (74, 76), (74, 78), (74, 79), (74, 86), (74, 90), (74, 96), (76, 50), (76, 51), (76, 59), (76, 60), 
    (76, 62), (76, 63), (76, 64), (76, 65), (76, 70), (76, 72), (76, 74), (76, 81), (76, 86), (76, 90), (76, 93), (76, 96), (76, 99), (77, 50), 
    (77, 60), (77, 90), (77, 97), (78, 51), (78, 52), (78, 65), (78, 76), (78, 82), (78, 99), (79, 53), (79, 55), (79, 57), (79, 60), (79, 62), 
    (79, 63), (79, 64), (79, 67), (79, 70), (79, 71), (79, 72), (79, 74), (79, 78), (79, 82), (79, 83), (79, 85), (79, 90), (79, 93), (79, 96), 
    (79, 99), (80, 2), (81, 53), (81, 55), (81, 60), (81, 70), (81, 76), (81, 79), (81, 92), (81, 93), (81, 96), (81, 99), (82, 78), (82, 79), (83, 53), (83, 57), (83, 58), (83, 67), (83, 72), (83, 79), (83, 81), (83, 88), (83, 92), (83, 93), (83, 96), (83, 98), (83, 99), (84, 55), (84, 57), (84, 69), (84, 88), (84, 91), (84, 93), (84, 94), (84, 98), (84, 99), (85, 79), (85, 91), (86, 62), (86, 74), (87, 60), (88, 54), (88, 55), (88, 56), (88, 57), (88, 58), (88, 67), (88, 68), (88, 69), (88, 70), (88, 79), (88, 83), (88, 84), (88, 91), (88, 94), (88, 95), (88, 96), (88, 98), (89, 61), (89, 73), (89, 95), (90, 50), (90, 51), (90, 52), (90, 60), (90, 64), (90, 65), (90, 74), (90, 76), (90, 86), (90, 93), (91, 55), (91, 57), (91, 72), (91, 79), (91, 84), (91, 85), (91, 88), (91, 94), (91, 96), (91, 98), (91, 99), (92, 54), (92, 55), (92, 56), (92, 57), (92, 69), (92, 73), (92, 83), (92, 95), (92, 98), (93, 52), (93, 53), (93, 62), (93, 63), (93, 68), (93, 72), (93, 76), (93, 77), (93, 78), (93, 79), (93, 81), (93, 83), (93, 84), (93, 90), (93, 96), (94, 19), (94, 54), (94, 55), (94, 57), (94, 58), (94, 69), (94, 79), (94, 81), (94, 83), (94, 84), (94, 88), (94, 91), (94, 98), (94, 99), (95, 55), (95, 56), (95, 58), (95, 61), (95, 73), (95, 88), (95, 89), (95, 92), (95, 94), (95, 98), (96, 2), (96, 46), (96, 55), (96, 64), (96, 70), (96, 72), (96, 74), (96, 76), (96, 79), (96, 81), (96, 83), (96, 88), (96, 91), (96, 93), (96, 98), (97, 11), (97, 44), (97, 45), (97, 77), (98, 53), (98, 55), (98, 56), (98, 57), (98, 58), (98, 69), (98, 72), (98, 79), (98, 83), (98, 84), (98, 85), (98, 88), (98, 91), (98, 92), (98, 94), (98, 95), (98, 96), (98, 99), (99, 50), (99, 53), (99, 57), (99, 58), (99, 67), (99, 70), (99, 71), (99, 72), (99, 76), (99, 78), (99, 79), (99, 81), (99, 83), (99, 91), (99, 94), (99, 98)]
    #[(11, 37), (19, 35), (30, 51), (30, 76), (44, 59), (44, 97), (45, 13), (45, 68), (45, 97), (48, 20), (48, 38), (50, 53), (50, 60), (50, 62), (50, 70), (50, 72), (50, 76), (50, 78), (50, 90), (51, 52), (51, 60), (51, 62), (51, 70), (51, 76), (51, 90), (52, 51), (52, 60), (52, 65), (52, 90), (52, 93), (53, 50), (53, 62), (53, 65), (53, 70), (53, 74), (53, 79), (53, 81), (53, 90), (53, 93), (53, 98), (53, 99), (55, 57), (55, 58), (55, 74), (55, 79), (55, 81), (55, 84), (55, 88), (55, 92), (55, 94), (55, 96), (55, 98), (57, 55), (57, 58), (57, 72), (57, 79), (57, 83), (57, 94), (57, 99), (58, 55), (58, 57), (58, 69), (58, 83), (58, 98), (58, 99), (60, 50), (60, 51), (60, 52), (60, 62), (60, 64), (60, 68), (60, 74), (60, 76), (60, 77), (60, 79), (60, 81), (60, 90), (62, 50), (62, 51), (62, 53), (62, 60), (62, 64), (62, 65), (62, 70), (62, 76), (62, 79), (62, 86), (62, 93), (63, 65), (63, 70), (63, 72), (63, 76), (63, 79), (63, 93), (64, 44), (64, 52), (64, 60), (64, 62), (64, 68), (64, 70), (64, 76), (64, 79), (64, 90), (64, 96), (65, 52), (65, 53), (65, 62), (65, 63), (65, 70), (65, 74), (65, 76), (65, 78), (67, 72), (67, 79), (67, 82), (67, 99), (68, 44), (68, 45), (68, 52), (68, 60), (68, 64), (68, 70), (68, 76), (68, 77), (68, 90), (69, 58), (69, 98), (69, 99), (70, 50), (70, 51), (70, 53), (70, 62), (70, 64), (70, 65), (70, 68), (70, 72), (70, 74), (70, 76), (70, 81), (70, 90), (70, 96), (70, 99), (71, 53), (71, 70), (71, 79), (72, 50), (72, 63), (72, 67), (72, 70), (72, 76), (72, 79), (72, 83), (72, 91), (72, 93), (72, 96), (72, 98), (72, 99), (74, 50), (74, 52), (74, 55), (74, 60), (74, 65), (74, 70), (74, 76), (74, 78), (74, 79), (74, 86), (74, 90), (74, 96), (76, 50), (76, 51), (76, 59), (76, 60), (76, 62), (76, 63), (76, 64), (76, 65), (76, 70), (76, 72), (76, 74), (76, 81), (76, 86), (76, 90), (76, 93), (76, 96), (76, 99), (77, 50), (77, 60), (77, 90), (77, 97), (78, 51), (78, 52), (78, 65), (78, 76), (78, 82), (78, 99), (79, 53), (79, 55), (79, 57), (79, 60), (79, 62), (79, 63), (79, 64), (79, 67), (79, 70), (79, 71), (79, 72), (79, 74), (79, 78), (79, 82), (79, 83), (79, 85), (79, 90), (79, 93), (79, 96), (79, 99), (81, 53), (81, 55), (81, 60), (81, 70), (81, 76), (81, 79), (81, 92), (81, 93), (81, 96), (81, 99), (82, 78), (82, 79), (83, 53), (83, 57), (83, 58), (83, 67), (83, 72), (83, 79), (83, 81), (83, 88), (83, 92), (83, 93), (83, 96), (83, 98), (83, 99), (84, 55), (84, 88), (84, 91), (84, 93), (84, 94), (85, 79), (85, 91), (86, 62), (86, 74), (88, 55), (88, 67), (88, 70), (88, 79), (88, 83), (88, 84), (88, 96), (88, 98), (90, 50), (90, 51), (90, 52), (90, 60), (90, 64), (90, 65), (90, 74), (90, 76), (90, 86), (90, 93), (91, 72), (91, 79), (91, 84), (91, 85), (91, 96), (91, 99), (92, 55), (92, 83), (92, 98), (93, 52), (93, 53), (93, 62), (93, 63), (93, 72), (93, 76), (93, 78), (93, 79), (93, 81), (93, 83), (93, 84), (93, 90), (93, 96), (94, 55), (94, 57), (94, 79), (94, 83), (94, 84), (96, 55), (96, 64), (96, 70), (96, 72), (96, 74), (96, 76), (96, 79), (96, 81), (96, 83), (96, 88), (96, 91), (96, 93), (96, 98), (97, 11), (97, 44), (97, 45), (97, 77), (98, 53), (98, 55), (98, 58), (98, 69), (98, 72), (98, 79), (98, 83), (98, 88), (98, 92), (98, 96), (98, 99), (99, 50), (99, 53), (99, 57), (99, 58), (99, 67), (99, 70), (99, 71), (99, 72), (99, 76), (99, 78), (99, 79), (99, 81), (99, 83), (99, 91), (99, 98)]
    #[(2, 45), (11, 9), (11, 12), (11, 37), (12, 11), (12, 18), (18, 20), (19, 35), (20, 18), (30, 51), (30, 59), (30, 64), (30, 68), (30, 76), (30, 97), (38, 20), (41, 49), (44, 59), (44, 97), (45, 13), (45, 30), (45, 36), (45, 68), (45, 97), (46, 11), (46, 68), (46, 77), (48, 20), (48, 38), (50, 53), (50, 60), (50, 62), (50, 70), (50, 72), (50, 76), (50, 78), (50, 90), (51, 52), (51, 60), (51, 62), (51, 70), (51, 76), (51, 90), (52, 51), (52, 60), (52, 65), (52, 90), (52, 93), (53, 50), (53, 62), (53, 65), (53, 70), (53, 74), (53, 79), (53, 81), (53, 90), (53, 93), (53, 98), (53, 99), (55, 57), (55, 58), (55, 74), (55, 79), (55, 81), (55, 84), (55, 88), (55, 92), (55, 94), (55, 96), (55, 98), (57, 55), (57, 58), (57, 72), (57, 79), (57, 83), (57, 94), (57, 99), (58, 55), (58, 57), (58, 69), (58, 83), (58, 98), (58, 99), (60, 44), (60, 50), (60, 51), (60, 52), (60, 62), (60, 64), (60, 68), (60, 74), (60, 76), (60, 77), (60, 79), (60, 81), (60, 90), (62, 50), (62, 51), (62, 53), (62, 60), (62, 64), (62, 65), (62, 70), (62, 76), (62, 79), (62, 86), (62, 93), (63, 65), (63, 70), (63, 72), (63, 76), (63, 79), (63, 93), (64, 30), (64, 44), (64, 52), (64, 60), (64, 62), (64, 68), (64, 70), (64, 76), (64, 79), (64, 90), (64, 96), (65, 52), (65, 53), (65, 62), (65, 63), (65, 70), (65, 74), (65, 76), (65, 78), (67, 72), (67, 79), (67, 82), (67, 99), (68, 30), (68, 44), (68, 45), (68, 52), (68, 60), (68, 64), (68, 70), (68, 76), (68, 77), (68, 90), (69, 58), (69, 98), (69, 99), (70, 50), (70, 51), (70, 53), (70, 62), (70, 64), (70, 65), (70, 68), (70, 72), (70, 74), (70, 76), (70, 81), (70, 90), (70, 96), (70, 99), (71, 53), (71, 70), (71, 79), (72, 50), (72, 63), (72, 67), (72, 70), (72, 76), (72, 79), (72, 83), (72, 91), (72, 93), (72, 96), (72, 98), (72, 99), (74, 50), (74, 52), (74, 55), (74, 60), (74, 65), (74, 70), (74, 76), (74, 78), (74, 79), (74, 86), (74, 90), (74, 96), (76, 50), (76, 51), (76, 59), (76, 60), (76, 62), (76, 63), (76, 64), (76, 65), (76, 70), (76, 72), (76, 74), (76, 81), (76, 86), (76, 90), (76, 93), (76, 96), (76, 99), (77, 50), (77, 60), (77, 90), (77, 97), (78, 51), (78, 52), (78, 65), (78, 76), (78, 82), (78, 99), (79, 53), (79, 55), (79, 57), (79, 60), (79, 62), (79, 63), (79, 64), (79, 67), (79, 70), (79, 71), (79, 72), (79, 74), (79, 78), (79, 82), (79, 83), (79, 85), (79, 90), (79, 93), (79, 96), (79, 99), (81, 53), (81, 55), (81, 60), (81, 70), (81, 76), (81, 79), (81, 92), (81, 93), (81, 96), (81, 99), (82, 78), (82, 79), (83, 53), (83, 57), (83, 58), (83, 67), (83, 72), (83, 79), (83, 81), (83, 88), (83, 92), (83, 93), (83, 96), (83, 98), (83, 99), (84, 55), (84, 88), (84, 91), (84, 93), (84, 94), (85, 79), (85, 91), (86, 62), (86, 74), (88, 55), (88, 67), (88, 70), (88, 79), (88, 83), (88, 84), (88, 96), (88, 98), (90, 50), (90, 51), (90, 52), (90, 60), (90, 64), (90, 65), (90, 74), (90, 76), (90, 86), (90, 93), (91, 72), (91, 79), (91, 84), (91, 85), (91, 96), (91, 99), (92, 55), (92, 83), (92, 98), (93, 52), (93, 53), (93, 62), (93, 63), (93, 72), (93, 76), (93, 78), (93, 79), (93, 81), (93, 83), (93, 84), (93, 90), (93, 96), (94, 55), (94, 57), (94, 79), (94, 83), (94, 84), (96, 53), (96, 55), (96, 64), (96, 70), (96, 72), (96, 74), (96, 76), (96, 79), (96, 81), (96, 83), (96, 88), (96, 91), (96, 93), (96, 98), (97, 11), (97, 30), (97, 36), (97, 44), (97, 45), (97, 77), (98, 53), (98, 55), (98, 58), (98, 69), (98, 72), (98, 79), (98, 83), (98, 88), (98, 92), (98, 96), (98, 99), (99, 50), (99, 53), (99, 57), (99, 58), (99, 67), (99, 70), (99, 71), (99, 72), (99, 76), (99, 78), (99, 79), (99, 81), (99, 83), (99, 91), (99, 98)]
    #appending curprice to prcall array. 
    curPrices = prices[-1, :]
    #print(curPrices)
    #new_prcAll = np.append(prcAll, curPrices)
    #prcAll = np.vstack([prcAll, curPrices])
    #print(prices.shape)
    #print(curPrices.shape)
    #print(curPrices)
    #print(new_prcAll.shape)

    for pair in pairs:
        #stock 74 8.96
        #stock 79 = 6,83
        if (prices[:, pair[0]] - prices[:, pair[1]]).mean() > 0:
            #pair[0] is > pair[1]
            stock_expensive = pair[0]
            stock_cheaper = pair[1]
        else:
            #pair[0] is < pair[1]
            stock_expensive = pair[1]
            stock_cheaper = pair[0]

        stock_expensive_price = prices[:, stock_expensive] #all the last prices of expensive stock rolling
        stock_cheaper_price = prices[:, stock_cheaper] #all the last prices of expensive stock rolling

        #get last 30 days of price series
        last_twenty = prices.shape[0] - 20

        stock_expensive_price = stock_expensive_price[last_twenty:]
        stock_cheaper_price = stock_cheaper_price[last_twenty:]

        #print(pair)
        (b, theo_spread) = getBetaCoeff(stock_cheaper_price, stock_expensive_price) #last 
        data_spread = stock_expensive_price - b * stock_cheaper_price
        #data_spread = prcAll[0:201, stock_expensive] - prcAll[0:201, stock_cheaper]
        mean_spread = data_spread.mean()        
        one_std = data_spread.std()
        
        #last_price_spread = curPrices[stock_expensive] - curPrices[stock_cheaper]
        last_price_spread = curPrices[stock_expensive] - b * curPrices[stock_cheaper]

        #standardize the price spread by subtracting the mean
        last_price_spread_standardized  = (last_price_spread - mean_spread)/one_std
        #Computing max sharesize
        #later it will be getShareSize()
        #sharesize_cheaper, sharesize_expensive = getShareSize(b,stock_cheaper, stock_expensive, curPrices)
        sharesize_expensive = 5000 // curPrices[stock_expensive]
        sharesize_cheaper = abs(b) * sharesize_expensive

        #STOPLOSS
        max_sharesize_cheaper = 10000 // curPrices[stock_cheaper]
        if abs(sharesize_cheaper) > abs(max_sharesize_cheaper):
            sharesize_cheaper = max_sharesize_cheaper

        #10000 z > 3       PAIR (A,B)                
        #9000  2 < z < 3
        #  1 < z < 2          

        #10000 z > 3      PAIR (C,D)
        #7000  2 < z < 3
        #5000  1 < z < 2
        if last_price_spread_standardized >= 2.5: #short the spread > 2 STD
            #long stock_cheaper
            #print(sharesize_cheaper)
            myPositions[stock_cheaper] = sharesize_cheaper
            #short stock_expensive
            myPositions[stock_expensive] = -sharesize_expensive
        
        elif last_price_spread_standardized >= 1 and last_price_spread_standardized < 2.5: #short the spread > 1SD
            #long stock_cheaper
            myPositions[stock_cheaper] = (sharesize_cheaper // 2) 
            #short stock_expensive
            myPositions[stock_expensive] = -(sharesize_expensive // 2)

        elif last_price_spread_standardized <= -2.5: #long the spread < - 2SD      
            #short stock_cheaper
            myPositions[stock_cheaper] = -sharesize_cheaper           
            #long stock_expensive 
            myPositions[stock_expensive] = sharesize_expensive

        elif last_price_spread_standardized <= -1 and last_price_spread_standardized > -2.5: #long the spread         
            #short stock_cheaper
            myPositions[stock_cheaper] = -(sharesize_cheaper // 2)            
            #long stock_expensive 
            myPositions[stock_expensive] = (sharesize_expensive // 2)
            
        elif last_price_spread_standardized <= (1/2.5) and last_price_spread_standardized >=0: #smaller than 1/3 std > 0 
            #if prevPositions[stock_cheaper] != 0 and prevPositions[stock_expensive] != 0: # we have a position
            myPositions[stock_cheaper] = 0
            myPositions[stock_expensive] = 0

        
        elif last_price_spread_standardized >= (-1/2.5) and last_price_spread_standardized <=0: #smaller than 1/3 std > 0 
            #if prevPositions[stock_cheaper] != 0 and prevPositions[stock_expensive] !=0: # we have a position
            myPositions[stock_cheaper] = 0 
            myPositions[stock_expensive] = 0

    return myPositions 

global prcSoFars
def getMyPosition (prcSoFar):
    global currentPos
    global prcSoFars
    (nins,nt) = prcSoFar.shape
    #prcSoFar = np.vstack([prcAll, prcSoFar.T])
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