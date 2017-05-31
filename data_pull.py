import os, sys, time
import datetime as dt
import pandas as pd
from pandas.io.data import DataReader

def getTickers(tickerPath):
    assert os.path.isfile(tickerPath)
    with open(tickerPath, 'rb') as f:
        tickers = [l.strip() for l in f.readlines()]
    return tickers

if __name__ == "__main__":
    assert((len(sys.argv) == 5)), 'Usage: python data_pull.py [start %Y%m%d ] [end %Y%m%d] [input_file] [output_file]'
    start = dt.datetime.strptime(sys.argv[1], '%Y%m%d')
    end = dt.datetime.strptime(sys.argv[2], '%Y%m%d')
    tickers = getTickers(sys.argv[3])
    data = {}
    for t in tickers:
        try:
            data[t] = DataReader(t, 'yahoo', start, end)
        except:
            print 'skipping %s' % (t,)
        time.sleep(3) #be nice
    panel = pd.Panel(data).swapaxes('minor', 'items')
    panel['Adj Close'].to_csv(sys.argv[4])
