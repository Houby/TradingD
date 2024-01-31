from bybit_basic_actions import *


def simple_moving_average(time_number, symbol):
    medium_data = []
    start_date = int(time.time() * 1000) - 43200000
    end_date = int(time.time() * 1000)

    for x in range(time_number):
        json_data = get_historical_interval(symbol=symbol, interval='240', start=start_date, end=end_date, limit='10')

        if json_data == "Error":
            return

        medium_data[time_number] = (float(json_data['result']["list"][x][4]) + float(json_data['result']["list"][x][1])) / 2

    current_moving_average = sum(medium_data)

    return current_moving_average

# def weight_moving_average

# def exponential_moving_average
