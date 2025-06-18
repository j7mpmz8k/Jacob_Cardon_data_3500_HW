import json
import requests
import time
directory_path = '/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/final_project/'
ticker = 'AAPL'


def import_stock(ticker):
    req = requests.get(f'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey=NG9C9EPVYBMQT0C8')
    time.sleep(12)
    raw_data = json.loads(req.text)

    #listing out available keys
    key1 = 'Time Series (Daily)'
    key2_date = '2025-06-16'#many more dates
    key3_open = '1. open'
    key3_high = '2. high'
    key3_low = '3. low'
    key3_close = '4. close'
    key3_volume = '5. volume'

    prices_w_dates = [f'{date_key},{raw_data[key1][date_key][key3_close]}\n' for date_key in raw_data[key1]]
    prices_w_dates.reverse()

    with open(f'{directory_path}{ticker}.csv', 'w') as new_file:
        new_file.writelines(prices_w_dates)

    return 

import_stock(ticker)



