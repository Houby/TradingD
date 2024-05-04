from bybit_basic_actions import *
from currencies import *

returnDataExchangeFirst = 64511.4
returnDataExchangeSecond = float(get_market_price(symbol='BTCUSDT'))
if not returnDataExchangeFirst or not returnDataExchangeSecond:
    pass
else:
    print(returnDataExchangeFirst, ", ", returnDataExchangeSecond)
    differentPercent = returnDataExchangeFirst / returnDataExchangeSecond
    print(differentPercent)
    if (differentPercent > 1.025):
        print('На первой бирже дороже.')
        # TODO: Добавить функцию покупки/продажи фьюча
    elif (differentPercent < 0.975):
        print('На первой бирже дешевле.')
        # TODO: Добавить функцию покупки/продажи фьюча
    else:
        print('Цена примерно одинаковая.')
        pass