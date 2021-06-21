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

def getRevenueGrowth(ticker):
    financials = yf.Ticker(ticker, session=session).quarterly_financials
    currentQuarter = str(financials.columns[0])
    nextQuarter = str(financials.columns[1])
    date1Revenue = financials.loc['Total Revenue', currentQuarter][0]
    date2Revenue = financials.loc['Total Revenue', nextQuarter][0]
    print(date1Revenue)
    print(date2Revenue)
    return (date1Revenue / date2Revenue) - 1

def calcMcap(yfTicker, price=0):
    '''
        @param yfTicker A yfinance Ticker object.
        @param price A number as stock price.
    '''

    if price < 0:
        price = ticker.info['previousClose']

    sharesOut = yfTicker.info['sharesOutstanding']

    return sharesOut * price

def calcEV(yfTicker, mCap):
    balanceSheet = yfTicker.balance_sheet
    currentQuarter = str(balanceSheet.columns[0])
    cash = balanceSheet.loc['Cash', currentQuarter][0]
    totalDebt = balanceSheet.loc['Long Term Debt', currentQuarter][0]

    return mCap + totalDebt - cash

def getEbitda(yfTicker):
    annual = yfTicker.financials.columns[0].strftime('%Y-%m-%d')
    ebit = yfTicker.financials.loc['Ebit', annual][0]
    da = yfTicker.cashflow.loc['Depreciation', annual][0]

    return ebit + da

def getGrossProfit(yfTicker):
    annual = yfTicker.financials.columns[0].strftime('%Y-%m-%d')
    return yfTicker.financials.loc['Gross Profit', annual][0]

def calcEvEbitda(yfTicker, ev):
    ebitda = getEbitda(yfTicker)
    return round(ev / ebitda)

def calcEvGP(yfTicker, ev):
    gp = getGrossProfit(yfTicker)
    return round(ev / gp)

def yCompare(tickers, price=0):
    ratios = {}

    for item in tickers:
        ticker = yf.Ticker(item, session=session)
        
        try:
            if price < 0:
                price = ticker.info['previousClose']

            evGp = math.ceil(getEvGp(ticker))
            evEbitda = math.ceil(ticker.info['enterpriseToEbitda'])
            ratios[item] = pd.Series({'Price $': price, 'EV/Gross Profit': evGp, 'EV/EBITDA': evEbitda})
        
        except:
            ratios[item] = pd.Series({'Price $': None, 'EV/Gross Profit': None, 'EV/EBITDA': None})
    
    return pd.DataFrame(ratios)

def sCompare(tickers, price=0):
    ratios = {}

    for item in tickers:
        ticker = yf.Ticker(item, session=session)
        
        try:
            if price < 0:
                price = ticker.info['previousClose']

            annual = ticker.financials.columns[0].strftime('%Y')

            mCap = calcMcap(ticker, price)
            ev = calcEV(ticker, mCap)
            evEbitda = calcEvEbitda(ticker, ev)
            evGP = calcEvGP(ticker, ev)

            ratios[item] = pd.Series({'Year': annual, 'Price $': price, 'EV/Gross Profit': evGP, 'EV/EBITDA': evEbitda})
        
        except Exception as e:
            print(f'Ticker {item} - {e}')
            ratios[item] = pd.Series({'Price $': None, 'EV/EBITDA': None})
    
    return pd.DataFrame(ratios)