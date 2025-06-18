import json


with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/test/large_test_data.json") as data:
    raw_data = json.load(data)

key1 = 'Time Series (Daily)'
key2_date = '2025-06-16'#many more dates
key3_open = '1. open'
key3_high = '2. high'
key3_low = '3. low'
key3_close = '4. close'
key3_volume = '5. volume'


for date_key in raw_data[key1]:
    print(raw_data[key1][date_key][key3_close])

