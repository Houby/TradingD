from get_env import api_key, secret_key
import time
import requests
import hmac
import hashlib
import json
import math

# создание хеша
def hashing(query_string):
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# запрос рыночной цены
def market_price(symbol, category='linear'):
    queryString = "category=" + category + "&symbol=" + symbol
    url = 'https://api.bybit.com/v5/market/tickers?' + queryString
    current_time = int(time.time() * 1000)
    sign = hashing(str(current_time) + api_key + '5000' + queryString)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.get(url=url, headers=headers)
    dataParsed = json.loads(response.text)
    lastMarketPrice = dataParsed['result']['list'][0]['lastPrice']
    return lastMarketPrice
