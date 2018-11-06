import urllib2
import urllib
import json
import fydates as fyd

CLIENT_ID = "dj0yJmk9TUtaYUV1WWVpeVY0JmQ9WVdrOWFVZG9RVFUyTkdNbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yNA--"
CLIENT_SECRET = "217b3fc3926c5e0253a5381da48261acdfa5d420"


def yql_req(yql):
    data = {
        "q":yql,
        "format":"json",
        "env":"store://datatables.org/alltableswithkeys"
    }
    url = "https://query.yahooapis.com/v1/public/yql"
    res = urllib2.urlopen(url,urllib.urlencode(data))
    return json.loads(res.read())
    

def historic_req(ticker,start_date,end_date):
    start_date = fyd.fromdate(start_date)
    end_date = fyd.fromdate(end_date)
    yql = 'select * from yahoo.finance.historicaldata where symbol = "' + ticker + '" and startDate = "' + start_date + '" and endDate = "' + end_date + '"'
    return yql_req(yql)

def quote_req(ticker):
    yql = 'select * from yahoo.finance.quotes where symbol = "'+ticker+'"'
    return yql_req(yql)

def get(d,*k):
    for _k in k:
        if _k in d:
            return d[_k]
    return None

def getf(d,*k):
    for _k in k:
        try:
            return float(d[_k])
        except:
            pass
    return None

def get_quote(d):
    if 'query' not in d:
        return None
    d = d['query']
    if 'results' not in d:
        return None
    d = d['results']
    if d is None:
        return None
    if 'quote' not in d:
        return None
    return d['quote']

def daily(ticker):
    d = get_quote(quote_req(ticker))
    if d is None:
        return None
    sym = get(d,'Symbol','symbol')
    pri = getf(d,'LastTradePriceOnly')
    bid = getf(d,'Bid')
    ask = getf(d,'Ask')
    vol = getf(d,'Volume')
    cur = get(d,'Currency')
    dhi = getf(d,'DaysHigh')
    dlo = getf(d,'DaysLow')
    ltd = get(d,'LastTradeDate')
    nme = get(d,'Name')
    opn = getf(d,'Open')
    
    
    return {
        "ticker":sym,
        "price":pri,
        "bid":bid,
        "ask":ask,
        "volume":vol,
        "currency":cur,
        "day_low":dlo,
        "day_high":dhi,
        "last_trade_date":ltd,
        "name":nme,
        "open_price":opn,
    }


def historic(ticker,start_date,end_date=fyd.today()):
    if isinstance(start_date,basestring):
        start_date = fyd.todate(start_date)
    if isinstance(end_date,basestring):
        end_date = fyd.todate(end_date)
    data = historic_req(ticker,start_date,end_date)
    data = get_quote(data)
    if data is None:
        return None
    return sorted(data,key=lambda x: fyd.todate(x['Date']))

def pp(d,l = 0):
    for k in d:
        if isinstance(d[k],dict):
            print l*'\t',k,":","{"
            pp(d[k],l+1)
            print l*'\t',"}"
        else:
            print l*'\t',k,":",d[k]

def aum(portfolio):
    aum = 0
    for ticker in port:
        aum += daily(ticker)["PRI"]*port[ticker]
    return aum

def E(x):
    return sum(x)/len(x)

def scov(x,y):
    if len(x) == 0 or len(y) == 0:
        return 0
    x0 = x[0]
    y0 = y[0]
    
    n = len(x)
    ex = 0
    ey = 0
    exy = 0
    for i in xrange(n):
        ex += x[i] - x0
        ey += y[i] - y0
        exy += (x[i] - x0)*(y[i] - y0)
    return (exy - (ex*ey)/n)/n

def beta(start_date,end_date,ticker,reference='^GSPC',return_range='daily'):
    A = historic(ticker,start_date,end_date)
    I = historic(reference,start_date,end_date)

    A = {a['Date']:float(a['Close']) for a in A}
    I = {i['Date']:float(i['Close']) for i in I}
    dates = sorted(list(set(A.keys()+I.keys())),key=lambda x: fyd.todate(x))
    with open('test.csv','w') as f:
        for date in dates:
            f.write(date+","+str(A[date])+","+str(I[date])+"\n")
    RA = []
    RI = []
    for i in xrange(len(dates)-1):
        RA.append((A[dates[i+1]]-A[dates[i]])/A[dates[i]])
        RI.append((I[dates[i+1]]-I[dates[i]])/I[dates[i]])
    return scov(RA,RI)/scov(RI,RI)

if __name__ == "__main__":
    sd = '2014-06-03'
    ed = '2015-06-03'
    print beta(sd,ed,'IBM',reference='GOOG')
    


