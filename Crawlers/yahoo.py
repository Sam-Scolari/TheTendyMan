import requests
from lxml import html

def get_website_url(ticker):
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

    response = requests.get(f'https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}', headers=headers)
    source = html.fromstring(response.content)

    return source.xpath('//*[@id="Col1-3-Profile-Proxy"]/section/div[1]/div/div/p[1]/a[2]')[0].text