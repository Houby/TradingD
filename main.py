import math

import schedule

from basic_actions import *
from currency_list import *


def market_open_order(symbol, side, order_type, qty, category='linear'):
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    current_crypto_price = get_market_price(symbol)
    count_zn = len(current_crypto_price.split('.')[1])

    if side == 'Sell':
        stop_loss = round(float(current_crypto_price) * 1.01, count_zn)
        take_profit = round(float(current_crypto_price) * 0.98, count_zn)
    elif side == 'Buy':
        stop_loss = round(float(current_crypto_price) * 0.99, count_zn)
        take_profit = round(float(current_crypto_price) * 1.02, count_zn)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{order_type}", "qty": "{qty}", "category": "{category}", "stopLoss": "{stop_loss}", "takeProfit": "{take_profit}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)


# Получение последних трёх свечей
def candles_imagine(symbol):
    data_out = ''
    start_date = int(time.time() * 1000) - 43200000
    end_date = int(time.time() * 1000)
    json_data = get_historical_interval(symbol=symbol, interval='240', start=start_date, end=end_date, limit='10')
    if json_data == "Error":
        return
    for x in range(3):
        cr_data = float(json_data['result']["list"][x][4]) - float(json_data['result']["list"][x][1])
        if cr_data > 0:
            # print('Свеча положительная')
            data_out = 'P' + data_out
        elif cr_data < 0:
            # print('Свеча отрицательная')
            data_out = 'M' + data_out
        else:
            # print('Свеча нулевая')
            data_out = 'O' + data_out
    return data_out


def open_trade(leverage):
    parse_n = 0
    for x in currency_list:
        symbol_ticker = x + currency_parameter
        parse_n += 1
        print(symbol_ticker)
        market_price = get_market_price(symbol=symbol_ticker)
        order_qnt = math.floor(17 / 100 * float(leverage) / float(market_price))
        data_out = candles_imagine(symbol=symbol_ticker)

        if data_out == 'MPP' or data_out == 'MPM' or data_out == 'MPO':
            set_leverage(symbol=symbol_ticker, buyLeverage=leverage, sellLeverage=leverage)
            market_open_order(symbol=symbol_ticker, side='Buy', order_type='Market', qty=order_qnt)
        if data_out == 'PMM' or data_out == 'PMP' or data_out == 'PMO':
            set_leverage(symbol=symbol_ticker, buyLeverage=leverage, sellLeverage=leverage)
            market_open_order(symbol=symbol_ticker, side='Sell', order_type='Market', qty=order_qnt)


def main():
    schedule.every().day.at('03:01').do(open_trade(leverage='25'))
    schedule.every().day.at('07:01').do(open_trade(leverage='25'))
    schedule.every().day.at('11:01').do(open_trade(leverage='25'))
    schedule.every().day.at('15:01').do(open_trade(leverage='25'))
    schedule.every().day.at('19:01').do(open_trade(leverage='25'))
    schedule.every().day.at('23:01').do(open_trade(leverage='25'))


if __name__ == "__main__":
    main()
