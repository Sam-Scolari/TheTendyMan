import json

with open('./Data/Reddit/Tickers/cciv.json', 'r') as file:
            
    json_ticker_data = json.loads(file.read())
    print(json_ticker_data)