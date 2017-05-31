"""
TDA_R.py

The TDA_R.py project defines functions that allow a user to analyze
financial stock data.

An ouput of daily adjacent closing prices for those stocks (CSV)
            sampling of corr data for few days (up to 256 companies) (XLS)
            plot of ripsDiag TDA result for few days (png)
            plot of Wasserstein distance for dimension 0, 1 (png)

With help from Alex Tseng, Portfolio Manager , Tower Research Capital
                       Marian Gidea, Research Advisor, Yeshiva University
"""

import sys
import pandas as pd
import datetime as dt
# import rpy2
# from rpy2.robjects import r
# # from rpy2.robjects.packages importr
#
# from rpy2.objects import pandas2ri
# pandas2ri.activate()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    #read data and drop nans
    df = pd.read_csv(sys.argv[1], parse_dates=True, index_col=0).dropna()
    #read data window period
    period = int(sys.argv[2])

    #read number of companies
    less256 = bool(sys.argv[3])

    #create pariwise Pearson correlation matrices, between -1 & 1.
    cor = df.rolling(window=period).corr(pairwise=True)
    cor = cor.reindex(df.index.date)

    #measure the distance Sqrt(2*(1-x)) between 0,2
    d = lambda x: round((2*(1-x))**.5, 4)
    dist = cor.apply(d)

    #this can be exported to an EXCEl for less than 256 companies
    if  less256:
        #upload that excel into R for TDA analysis.
        dist.to_excel("outputD.xls")

    #Run r from Python. use r() to write in R
    i=0 #keep count between python & r loops
    r("Diag[]=list()") # to hold data
    r("maxdimension=2") # max dimension to look for in data
    r("maxscale=2")

    for day in dist.items:
        i+=1
        X=dist[day]
        r.assign("X", X)
        r.assign("i", i)
        r("Diag[[i]]=ripsDiag(X, maxdimension, maxscale, dist=""arbitrary"" \
            ,library=""Dionysus"", printProgress=TRUE)$diagram")
    r("plot(Diag[[15]])")
    r("plot(Diag[[115]])")
    r("plot(Diag[[1000]])")
