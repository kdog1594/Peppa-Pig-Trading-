import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from statsmodels.tsa.stattools import coint
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(suppress=True)
def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices250.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

my_array = np.ones((100,100), dtype="f") #dtype="f,f"
i = 0
j = 0
for stock in prcAll:
    j = 0
    #outer for loop (testing stock 1 against all the others...)
    for iterate in prcAll:
        #correlation = np.corrcoef(stock, iterate)
        if i != j: 
            #print("debug1")
            score, pvalue, array = coint(stock, iterate)
            #print("debug2")
            if pvalue < 0.025:
                    my_array[i,j] = pvalue
        #add the correlation and coint to numpy array
       # rounded = round(correlation[0,1],3)       
        j += 1   

    i+=1

print(my_array)
#converting to pandas dataframe and dumping in txt file
np.savetxt("pvalue1.csv", my_array, delimiter=",")