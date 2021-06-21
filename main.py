from utils import sCompare, yCompare
import yfinance as yf
import json

#nowTicker = yf.Ticker('NOW')

tickerList = ['NOW']
#print(yCompare(tickerList, 534.75))
print(sCompare(tickerList, 534.75))

#print(nowTicker.info['previousClose'])

#growth = getRevenueGrowth('SQ')
#print('{:.2%}'.format(growth))