import datetime

YQL_DATE_FORMAT = '%Y-%m-%d'

def todate(date,fmt=YQL_DATE_FORMAT):
    return datetime.datetime.strptime(date,fmt)

def fromdate(date,fmt=YQL_DATE_FORMAT):
    return date.strftime(fmt)

def today():
    return datetime.datetime.today()
