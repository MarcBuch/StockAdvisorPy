from utils import compare, getRevenueGrowth
import yfinance as yf
import json

tickerStr = ['NOW', 'DOCU', 'TWLO', 'WDAY', 'SQ', 'Z', 'PTON']
print(compare(tickerStr))

#growth = getRevenueGrowth('SQ')
#print('{:.2%}'.format(growth))