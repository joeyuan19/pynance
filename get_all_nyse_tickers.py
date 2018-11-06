import urllib2
from lxml import etree

def write(ticker,exchange):
    ticker = ticker.strip()
    if len(ticker) > 0:
        with open('tickers/'+exchange+'.txt','a') as f:
            f.write(exchange+","+ticker+'\n')
    
def get_text(node):
    return ''.join(node.itertext())

def scrape_names(html,exchange):
    node = etree.HTML(html)
    for i in node.findall(r'.//tr[@class="ro"]/td/a'):
        write(get_text(i),exchange)
    for i in node.findall(r'.//tr[@class="re"]/td/a'):
        write(get_text(i),exchange)

def get_page(url):
    return urllib2.urlopen(url).read()


def gen_url(exchange,letter):
    return "http://www.eoddata.com/stocklist/"+exchange+"/"+letter+".htm"

def scrape_page(exchange,letter):
    scrape_names(get_page(gen_url(exchange,letter)),exchange)

def scrape(exchange):
    for i in xrange(26):
        scrape_page(exchange,chr(ord('A')+i))
    for i in xrange(10):
        scrape_page(exchange,str(i))
        


exchanges = [
    'AMEX',
    'AMS',
    'ASX',
    'BRU',
    'CBOT',
    'CFE',
    'CME',
    'COMEX',
    'EUREX',
    'FOREX',
    'HKEX',
    'INDEX',
    'KCBT',
    'LIFFE',
    'LIS',
    'LSE',
    'MGEX',
    'MLSE',
    'MSE',
    'NASDAQ',
    'NYBOT',
    'NYMEX',
    'NYSE',
    'NZX',
    'OPRA',
    'OTCBB',
    'PAR',
    'SGX',
    'TSX',
    'TSXV',
    'USMF',
    'WCE'
]

if __name__ == '__main__':
    for exchange in exchanges:
        open('tickers/'+exchange + '.txt','w').close()
        scrape(exchange)
