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
def get_market_price(symbol, category='linear'):
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

# отмена всех ордеров по тикеру
def cancel_all_order(symbol, category='linear'):
    url = 'https://api.bybit.com/v5/order/cancel-all'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)

# установка плечей
def set_leverage(symbol, buyLeverage, sellLeverage, category='linear'):
    url = 'https://api.bybit.com/v5/position/set-leverage'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "buyLeverage": "{buyLeverage}", "sellLeverage": "{sellLeverage}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)

# запрос баланса аккаунта
def get_wallet_balance(accountType='CONTRACT', coin='USDT'):
    queryString = "accountType=" + accountType + "&coin=" + coin
    url = 'https://api.bybit.com/v5/account/wallet-balance?' + queryString
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
    realWalletBalance = float(dataParsed['result']['list'][0]['coin'][0]['walletBalance'])
    return realWalletBalance

def get_position_info(symbol, category='linear'):
    queryString = "category=" + category + "&symbol=" + symbol
    url = 'https://api.bybit.com/v5/position/list?' + queryString
    current_time = int(time.time() * 1000)
    sign = hashing(str(current_time) + api_key + '5000' + queryString)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.get(url=url, headers=headers)
    print(response.text)
    dataParsed = json.loads(response.text)
    if float(dataParsed['result']['list'][0]['size']) != 0:
        createOrderTime = dataParsed['result']['list'][0]['updatedTime']
        orderSize = dataParsed['result']['list'][0]['size']
        orderSide = dataParsed['result']['list'][0]['side']
        print(createOrderTime, orderSize, orderSide)
        return [createOrderTime, orderSize, orderSide]
    else:
        return "error"

def create_symbol(currency_list, currency_parameter):
    return currency_list + currency_parameter

def get_historical_interval(symbol, interval, start, end, limit, category='linear'):
    queryString = "category=" + category + "&symbol=" + symbol + "&interval=" + interval + "&start=" + str(start) + "&end=" + str(end) + "&limit=" + limit
    url = 'https://api.bybit.com/v5/market/kline?' + queryString
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
    if dataParsed['retMsg'] == 'OK':
        return(dataParsed)
    else:
        return "error"