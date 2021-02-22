import requests
from lxml import html
import json

headers = {
    'authority': 'finance.yahoo.com',
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

def fetch(ticker):
    response1 = requests.get(f'https://finance.yahoo.com/quote/{ticker}', headers=headers)
    source1 = html.fromstring(response1.content)

    response2 = requests.get(f'https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}', headers=headers)
    source2 = html.fromstring(response2.content)

    link = source2.xpath('//*[@id="Col1-3-Profile-Proxy"]/section/div[1]/div/div/p[1]/a[2]')[0].text

    data = {
        'ticker': ticker,
        'business_name': (source1.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')[0].text).split(' - ')[1],
        'website': link,
        'image': f'https://logo.clearbit.com/{link}',
        'exchange': (source1.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span')[0].text).split(' - ')[0],
        'stock_price': source1.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/span')[0].text,
        'last_close': source1.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span')[0].text,
        'open': source1.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span')[0].text,
        'volume': source1.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span')[0].text,
        'avg_volume': source1.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span')[0].text,
        'market_cap': source1.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span')[0].text,
    }

    return json.dumps(data)
