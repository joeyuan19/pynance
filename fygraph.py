import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker
from fynance import historic, fromdate, todate
import datetime

def format_date(x, pos=None):
    return x.strftime('%Y-%m-%d')

def chart(ticker,date1,date2):
    prices = historic(ticker,date1,date2)
    if len(prices) > 0:
        x,y = [],[]
        for price in prices:
            x.append(todate(price['Date']))
            y.append(price['Close'])
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.plot(x,y)
        fig.autofmt_xdate()
        plt.show()

def chart_all(date1,date2,ticker):


chart("IBM",todate("2005-04-25"),datetime.datetime.today())



