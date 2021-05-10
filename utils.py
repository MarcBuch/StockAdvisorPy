import yfinance as yf
import pandas as pd
import math
import requests_cache

session = requests_cache.CachedSession('yfinance.cache')

def getEvEbitda(ticker):
    annual = ticker.financials.columns[0].strftime('%Y-%m-%d')

    ev = ticker.info['enterpriseValue']
    ebit = ticker.financials.loc['Ebit', annual][0]
    da = ticker.cashflow.loc['Depreciation', annual][0]

    ebitda = ebit + da
    return ev / ebitda

def getEvGp(ticker):
    annual = ticker.financials.columns[0].strftime('%Y-%m-%d')
    enterpriseValue = ticker.info['enterpriseValue']
    grossProfit = ticker.financials.loc['Gross Profit', annual][0]

    return enterpriseValue / grossProfit

def compare(tickers):
    ratios = {}

    for item in tickers:
        ticker = yf.Ticker(item, session=session)
        
        try:
            evEbitda = math.ceil(ticker.info['enterpriseToEbitda'])
            evGp = math.ceil(getEvGp(ticker))
            ratios[item] = pd.Series({'EV/EBITDA': evEbitda, 'EV/Gross Profit': evGp})
        
        except:
            ratios[item] = pd.Series({'EV/EBITDA': None, 'EV/Gross Profit': None})
    
    return pd.DataFrame(ratios)

def getRevenueGrowth(ticker):
    financials = yf.Ticker(ticker, session=session).quarterly_financials
    currentQuarter = str(financials.columns[0])
    nextQuarter = str(financials.columns[1])
    date1Revenue = financials.loc['Total Revenue', currentQuarter][0]
    date2Revenue = financials.loc['Total Revenue', nextQuarter][0]
    print(date1Revenue)
    print(date2Revenue)
    return (date1Revenue / date2Revenue) - 1