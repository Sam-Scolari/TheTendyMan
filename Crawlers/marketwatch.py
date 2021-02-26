import requests
from lxml import html
import json
from bs4 import BeautifulSoup
from Crawlers import yahoo

def get_quote(ticker):
    headers = {
        'authority': 'marketwatch.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }

    response = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}', headers=headers)
    source = html.fromstring(response.content)

    link = yahoo.get_website_url(ticker)

    data = {
        'ticker': ticker,
        'business-name': source.cssselect('body > div.container.container--body > div.region.region--intraday > div:nth-child(2) > div > div:nth-child(2) > h1')[0].text,
        'website': link,
        'image':  f'https://logo.clearbit.com/{link}',
        'exchange': (source.cssselect('body > div.container.container--body > div.region.region--intraday > div:nth-child(2) > div > div:nth-child(1) > div.company__symbol > span.company__market')[0].text).split(': ')[1],
        'price': source.cssselect('body > div.container.container--body > div.region.region--intraday > div.column.column--aside > div > div.intraday__data > h3 > bg-quote')[0].text,
        'price-change': source.cssselect('body > div.container.container--body > div.region.region--intraday > div.column.column--aside > div > div.intraday__data > bg-quote > span.change--point--q > bg-quote')[0].text,
        'percent-change': source.cssselect('body > div.container.container--body > div.region.region--intraday > div.column.column--aside > div > div.intraday__data > bg-quote > span.change--percent--q > bg-quote')[0].text,
        'last-close': (source.cssselect('body > div.container.container--body > div.region.region--intraday > div.column.column--aside > div > div.intraday__close > table > tbody > tr > td')[0].text).replace('$', ''),
        'open': (source.cssselect('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.left > div > ul > li:nth-child(1) > span.primary')[0].text).replace('$', ''),
        'volume': source.cssselect('body > div.container.container--body > div.region.region--intraday > div.column.column--full.supportive-data > mw-rangebar.element.element--range.range--volume > div.range__header > span.primary')[0].text,
        'avg-volume': source.cssselect('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.left > div > ul > li:nth-child(16) > span.primary')[0].text,
        'market-cap': source.cssselect('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.left > div > ul > li:nth-child(4) > span.primary')[0].text,
    }

    return json.dumps(data)

def get_tick_data(ticker):
    response = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}/download-data?mod=mw_quote_tab', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    date = []
    open = []
    high = []
    low = []
    close = []
    volume = []
   
    table = soup.find_all('table')
    for row in table[4].find_all('tr'):
        i = 0
        for item in row.find_all('td'):
            if i == 0:
                date.append(item.text.split('\n')[1])
            elif i == 1:
                open.append(item.text.replace('$', ''))
            elif i == 2:
                high.append(item.text.replace('$', ''))
            elif i == 3:
                low.append(item.text.replace('$', ''))
            elif i == 4:
                close.append(item.text.replace('$', ''))
            elif i == 5:
                volume.append(item.text)
            i+=1
    
    data = {'date':date, 'open':open, 'high':high, 'low':low,'close':close, 'Volume':volume}

    return json.dumps(data)

def get_sec_filing(ticker):
    headers = {
        'authority': 'marketwatch.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }

    response = requests.get(f'https://www.marketwatch.com/investing/stock/{ticker}/financials/secfilings', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    filing_date = []
    document_type = []
    category = []
    
    table = soup.find_all('table')

    for row in table[4].find_all('tr'):
        i = 0
        for item in row.find_all('td'):
            if i == 0:
                filing_date.append(item.text.split('\n')[1])
            elif i == 2:
                links = item.findChildren('a')    
                document_type.append([item.text, links[0]['href']])

            elif i == 3:
                category.append(item.text)
            i+=1
    
    data = {'filing-date': filing_date, 'document-type': document_type, 'category': category}

    return json.dumps(data)
