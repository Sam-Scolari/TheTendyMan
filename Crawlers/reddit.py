import requests
from english_words import english_words_set
from Crawlers import marketwatch
import json

def get_posts(subreddit):
    headers = {
        'authority': 'www.reddit.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'edgebucket=oCe5to07mFePKzFEpr; __gads=ID=e93d0903f6b5f56b:T=1573598771:S=ALNI_MbSF5Ea8bHJpI7OjI1lSvHJAkvZTQ; reddaid=VH6LNQGE2TXPQYIA; over18=1; csv=1; pc=us; __stripe_mid=5d138923-bc72-4b15-82f2-1009e6a6abafba3292; G_ENABLED_IDPS=google; reddit_session=629947110711^%^2C2020-09-10T15^%^3A49^%^3A06^%^2C99b40e7c23967477a522ceaa977d13e744abde81; loid=000000000081e68th3.2.1599716759073.Z0FBQUFBQmZZNG1fT0g4M3dpZnd5N2F4NjczRzhFUEJqbU9aaGNRNUVKOTd5R0pHMVM2Z0VhSldJRHRfdkhRcTgzMENrZHRkQkFxa3pucEdlWlRQVzJkbmR0NmVtY2hmdGFMNVcwQzFGZVpUaU1DUzNDUlgyN2llRmQtS3ZKRU4xNDh1V2huTUgzSWM; d2_token=3.f89f24687eb943d771aeed939f854d4c31a2663c6806167fc774946e585af15a.eyJhY2Nlc3NUb2tlbiI6IjYyOTk0NzExMDcxMS1IZGN6RllvbGVGU0ZuMWtKT2d0M0JvR3NEX00iLCJleHBpcmVzIjoiMjAyMC0xMS0xMFQwNjoxNDozMy4wMDBaIiwibG9nZ2VkT3V0IjpmYWxzZSwic2NvcGVzIjpbIioiLCJlbWFpbCJdfQ==; USER=eyJsYW5ndWFnZSI6ImVuIiwicHJlZnMiOnsibGF5b3V0IjoiY2FyZCIsImdsb2JhbFRoZW1lIjoiTklHSFQiLCJjb2xsYXBzZWRUcmF5U2VjdGlvbnMiOnsiZmF2b3JpdGVzIjpmYWxzZSwibXVsdGlzIjpmYWxzZSwibW9kZXJhdGluZyI6ZmFsc2UsInN1YnNjcmlwdGlvbnMiOmZhbHNlLCJwcm9maWxlcyI6ZmFsc2V9LCJuaWdodG1vZGUiOnRydWUsInN1YnNjcmlwdGlvbnNQaW5uZWQiOmZhbHNlLCJycGFuRHVEaXNtaXNzYWxUaW1lIjpudWxsLCJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6bnVsbCwidG9wQ29udGVudFRpbWVzRGlzbWlzc2VkIjowfX0=; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=^%^220ae22fd4-aeea-4c56-8979-cfaf936c541d^%^22; show_announcements=yes; __aaxsc=1; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTMyNTQ1NTAsInN1YiI6IjYyOTk0NzExMDcxMS1UcEVRYTRrVnVOeG9xTlI0dlBfN1djcUQ0YmsiLCJsb2dnZWRJbiI6dHJ1ZSwic2NvcGVzIjpbIioiLCJlbWFpbCJdfQ.LDNKxvJ_c7imV-Q2CKr0ikBbVR8v0v87gdjLb1oHEMI; Psalm20_7-9_recentclicks2=t3_pmrdu^%^2Ct3_cte3jc^%^2Ct3_deyapq; recent_srs=t5_2ohexx^%^2Ct5_2sjdt^%^2Ct5_2qzb6^%^2Ct5_2qwj8^%^2Ct5_2rjsc^%^2Ct5_2qh8e^%^2Ct5_2qhor^%^2Ct5_3hr9s^%^2Ct5_2qjfk^%^2Ct5_2r05i; session=2f5e58dfb8d7983128502fc95c72c5c56aed0ed6gASVSQAAAAAAAABKe0UoYEdB2An+I7OPen2UjAdfY3NyZnRflIwoYWQzMzM1N2E5NmI3NjRlM2YxNjYyNzRlOGIwNzAxN2U2OTE1ZmU0MZRzh5Qu; aasd=3^%^7C1613251404962; session_tracker=qhdbbfdecoeinmrbbq.0.1613252067096.Z0FBQUFBQmdLRVhqc1RCQUNjYWphWDduR18wOXVpd3dwdWgyUHpLSlRXN0VFVGhjVmRJSVVyRm90LWpJQjhrTldTeFNuLW4tbk9vZFVUTW9VdXlzOTVQRHBscHdZX1UxMjRTRjd2TUVneFlzTFVQNHZfZDBZdHdxenlCLW5pM01IMUFLX3pqUUZub3c',
    }
    response = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?limit=100', headers=headers)
    json_response = response.json()

    posts = [post['data']['permalink'] for post in json_response['data']['children']]
    return posts

def parse_post(post):
    headers = {
        'authority': 'www.reddit.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'edgebucket=oCe5to07mFePKzFEpr; __gads=ID=e93d0903f6b5f56b:T=1573598771:S=ALNI_MbSF5Ea8bHJpI7OjI1lSvHJAkvZTQ; reddaid=VH6LNQGE2TXPQYIA; over18=1; csv=1; pc=us; __stripe_mid=5d138923-bc72-4b15-82f2-1009e6a6abafba3292; G_ENABLED_IDPS=google; reddit_session=629947110711^%^2C2020-09-10T15^%^3A49^%^3A06^%^2C99b40e7c23967477a522ceaa977d13e744abde81; loid=000000000081e68th3.2.1599716759073.Z0FBQUFBQmZZNG1fT0g4M3dpZnd5N2F4NjczRzhFUEJqbU9aaGNRNUVKOTd5R0pHMVM2Z0VhSldJRHRfdkhRcTgzMENrZHRkQkFxa3pucEdlWlRQVzJkbmR0NmVtY2hmdGFMNVcwQzFGZVpUaU1DUzNDUlgyN2llRmQtS3ZKRU4xNDh1V2huTUgzSWM; d2_token=3.f89f24687eb943d771aeed939f854d4c31a2663c6806167fc774946e585af15a.eyJhY2Nlc3NUb2tlbiI6IjYyOTk0NzExMDcxMS1IZGN6RllvbGVGU0ZuMWtKT2d0M0JvR3NEX00iLCJleHBpcmVzIjoiMjAyMC0xMS0xMFQwNjoxNDozMy4wMDBaIiwibG9nZ2VkT3V0IjpmYWxzZSwic2NvcGVzIjpbIioiLCJlbWFpbCJdfQ==; USER=eyJsYW5ndWFnZSI6ImVuIiwicHJlZnMiOnsibGF5b3V0IjoiY2FyZCIsImdsb2JhbFRoZW1lIjoiTklHSFQiLCJjb2xsYXBzZWRUcmF5U2VjdGlvbnMiOnsiZmF2b3JpdGVzIjpmYWxzZSwibXVsdGlzIjpmYWxzZSwibW9kZXJhdGluZyI6ZmFsc2UsInN1YnNjcmlwdGlvbnMiOmZhbHNlLCJwcm9maWxlcyI6ZmFsc2V9LCJuaWdodG1vZGUiOnRydWUsInN1YnNjcmlwdGlvbnNQaW5uZWQiOmZhbHNlLCJycGFuRHVEaXNtaXNzYWxUaW1lIjpudWxsLCJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6bnVsbCwidG9wQ29udGVudFRpbWVzRGlzbWlzc2VkIjowfX0=; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=^%^220ae22fd4-aeea-4c56-8979-cfaf936c541d^%^22; show_announcements=yes; __aaxsc=1; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTMyNTQ1NTAsInN1YiI6IjYyOTk0NzExMDcxMS1UcEVRYTRrVnVOeG9xTlI0dlBfN1djcUQ0YmsiLCJsb2dnZWRJbiI6dHJ1ZSwic2NvcGVzIjpbIioiLCJlbWFpbCJdfQ.LDNKxvJ_c7imV-Q2CKr0ikBbVR8v0v87gdjLb1oHEMI; Psalm20_7-9_recentclicks2=t3_pmrdu^%^2Ct3_cte3jc^%^2Ct3_deyapq; recent_srs=t5_2ohexx^%^2Ct5_2sjdt^%^2Ct5_2qzb6^%^2Ct5_2qwj8^%^2Ct5_2rjsc^%^2Ct5_2qh8e^%^2Ct5_2qhor^%^2Ct5_3hr9s^%^2Ct5_2qjfk^%^2Ct5_2r05i; session=2f5e58dfb8d7983128502fc95c72c5c56aed0ed6gASVSQAAAAAAAABKe0UoYEdB2An+I7OPen2UjAdfY3NyZnRflIwoYWQzMzM1N2E5NmI3NjRlM2YxNjYyNzRlOGIwNzAxN2U2OTE1ZmU0MZRzh5Qu; aasd=3^%^7C1613251404962; session_tracker=qhdbbfdecoeinmrbbq.0.1613252067096.Z0FBQUFBQmdLRVhqc1RCQUNjYWphWDduR18wOXVpd3dwdWgyUHpLSlRXN0VFVGhjVmRJSVVyRm90LWpJQjhrTldTeFNuLW4tbk9vZFVUTW9VdXlzOTVQRHBscHdZX1UxMjRTRjd2TUVneFlzTFVQNHZfZDBZdHdxenlCLW5pM01IMUFLX3pqUUZub3c',
    }

    response = requests.get(f'https://www.reddit.com/{post[:-1]}.json', headers=headers)
    json_response = response.json()

    num_comments = json_response[0]['data']['children'][0]['data']['num_comments']
    score = json_response[0]['data']['children'][0]['data']['score']
    created = json_response[0]['data']['children'][0]['data']['created']

    body = json_response[0]['data']['children'][0]['data']['selftext']
    words = body.split(' ')

    possible_tickers = []

    # Remove symbols and other unecessary characters from a string
    def clean(word):
        symbols = ['\n', '\t', '$', '%', '#', '@', '!', '?', '.', '"', '\'', '[', ']', '{', '}', '(', ')', '*', '&', '^', '`', '~', '=', '+', '-', '_', '/', '<', '>', ';', ':', '\\', '|']
        for char in word:
            for i in range(0, len(symbols)):
                if symbols[i] == char:
                    word = word.replace(symbols[i], '')
        return word

    # Attempt to identify tickers within a string of text
    for word in words:
        clean_word = clean(word).lower()
        if len(word) > 0:
            if word[0] == '$' or word == word.upper():
                possible_tickers.append(clean_word)

            elif len(clean_word) < 6 and clean_word not in english_words_set:
                possible_tickers.append(clean_word)

    # Remove any duplicate tickers
    tickers = []
    [tickers.append(ticker) for ticker in possible_tickers if ticker not in tickers]

    # Confirm whether each ticker is infact an actual ticker
    for ticker in tickers:
        if marketwatch.get_quote(ticker) == -1:
            tickers.remove(ticker)

    ticker_data = {'date': created, 'link': post, 'likes': score, 'replies': num_comments}

    # Read and update the saved ticker data
    for ticker in tickers:
        with open(f'./Data/Reddit/Tickers/{ticker}.json', 'a+') as file:
            try: 
                saved_ticker_data = json.loads(file.read())

            except Exception as e:
                print(e)


    return ticker_data

# print(parse_post(get_posts('SPACs')[0]))
