import schedule

from basic_actions import *


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


def open_trade():
    return


def main():
    schedule.every().day.at('03:01').do(open_trade)
    schedule.every().day.at('07:01').do(open_trade)
    schedule.every().day.at('11:01').do(open_trade)
    schedule.every().day.at('15:01').do(open_trade)
    schedule.every().day.at('19:01').do(open_trade)
    schedule.every().day.at('23:01').do(open_trade)


if __name__ == "__main__":
    main()
