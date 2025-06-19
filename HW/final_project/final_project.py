import json
import requests
import time
directory_path = '/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/final_project/'
#tickers = ['AAPL', 'ADBE', 'META', 'AMZN', 'COIN', 'GOOG', 'HOOD', 'NVDA', 'TSLA', 'VOO']
tickers = ['AAPL', 'ADBE']

#reads all files from "stock_files" variable. 
#Returns ticker and prices to be passed into trading strategy calculation functions along with functions to save to dictionary and .json file
def import_stock(ticker):
    # req = requests.get(f'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey=NG9C9EPVYBMQT0C8')
    # time.sleep(12)
    # raw_data = json.loads(req.text)#.loads() used instead of .load() since json dictionary is contained within a string
    # #listing out available keys
    # key1 = 'Time Series (Daily)'
    # key2_date = '2025-06-16'# Note! many more dates
    # key3_open = '1. open'
    # key3_high = '2. high'
    # key3_low = '3. low'
    # key3_close = '4. close'
    # key3_volume = '5. volume'

    # try:
    #     with open(f'{directory_path}{ticker}.csv', 'r') as csv_file:
    #         lines = csv_file.readlines()
    #         last_date = lines[-1].split(',')[0]
    #     new_lines = []

    #     #pulls all close prices in all dates
    #     for date_key in raw_data[key1]:
    #         if date_key > last_date:
    #             new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_volume]),2)},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
    #     new_lines.reverse()

    #     with open(f'{directory_path}{ticker}.csv', 'a') as csv_file:
    #         csv_file.writelines(new_lines)
    #     print('found existing file, appending new data')
    # except (FileNotFoundError, IndexError):
    #     print('\nERROR! file not found or file is empty. Recreating file.')
    #     new_lines = []
    #     #pulls all close prices in all dates
    #     for date_key in raw_data[key1]:
    #         new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_volume]),2)},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
    #     new_lines.reverse()

    #     with open(f'{directory_path}{ticker}.csv', 'w') as csv_file:
    #         csv_file.writelines(new_lines)

    with open(f'{directory_path}{ticker}.csv', 'r') as csv_file:
        lines = csv_file.readlines()
        prices = []
        for line in lines:
            prices.append(float(line.split(',')[-1].strip()))
    return prices

#calculates previous "N_days" moving average along with error preventions ensuring "N_days" are available to calculate
#pulls price data passed down from functions
def last_N_day_avg_from(prices, N_days, day=0):
    dayN = day
    day1 = day-N_days
    if day1 < 0:
        return print(f'\nERROR! Day must be no less than {N_days} and no more than {len(prices)} \n')
    return sum(prices[day1:dayN])/N_days


# calculates & prints trading strategy with at 2% difference from "N_days" moving average
def meanReversionStrategey(ticker, prices):
    N_days = 200# executes strategy over Nth number of days
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} Mean Reversion Strategy Over Period of: {N_days}')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day > N_days:# ensures at least "N_days" have past till "N_days" average calculates

            #ensures today's price is at least 2% less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price > last_N_day_avg_from(prices, N_days, day)*1.02 and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should sell at:\t$ {price}')
                    print(f'trade profits:\t$ {trade_profits}')
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price < last_N_day_avg_from(prices, N_days, day)*0.98 and buy == 0:#buy conditions
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should buy at:\t\t$ {price}')
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit/first_buy)*100,2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}')
    return total_profit, final_profit_percentage

# calculates & prints trading strategy with any difference from "N_days" moving average inverted from meanReversionStrategey
def simpleMovingAverageStrategy(ticker, prices):
    N_days = 5# executes strategy over Nth number of days

    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} Simple Moving Average Strategy Output Over Period of: {N_days}')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day > N_days:# ensures at least "N_days" days have past till "N_days" average calculates

            #ensures today's price is less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price < last_N_day_avg_from(prices, N_days, day) and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should sell at:\t$ {price}')
                    print(f'trade profits:\t$ {trade_profits}')
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price > last_N_day_avg_from(prices, N_days, day) and buy == 0:#buy conditions
                if day == len(prices)-1:# checks if day is most recent day
                    print(f'Today you should buy at:\t\t$ {price}')
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit/first_buy)*100,2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}')
    print('-'*44)#creates a line for formatting
    return total_profit, final_profit_percentage

#sets up dictionary of trading analysis preparatory to exporting to .json
returns = {}
# executes calculations of trading strategies
def analyze_stocks(ticker, prices):
    returns[f'{ticker}_prices'] = prices
    mr_profit, mr_returns = meanReversionStrategey(ticker, prices)
    sma_profit, sma_returns = simpleMovingAverageStrategy(ticker, prices)
    returns[f'{ticker}_mr_profit'] = mr_profit
    returns[f'{ticker}_mr_returns'] = mr_returns
    returns[f'{ticker}_sma_profit'] = sma_profit
    returns[f'{ticker}_sma_returns'] = sma_returns

#exports dictionary to .json file
def saveResults(dictionary):
    with open(f'{directory_path}results.json', 'w') as file:
        json.dump(dictionary, file, indent=4)
    print(f'\n"results.json" saved to: {directory_path}\n')

#################################################################################################################################################

# execution script to open, read, perform analysis, and save to dictionary
for ticker in tickers:
    prices = import_stock(ticker)# finds files from directory variable, reads data and extracts ticker from file name and price data within file
    analyze_stocks(ticker, prices)# calculates trading trading strategies and saves analysis to dictionary

#writes saved dictionary to results.json file to directory path variable
saveResults(returns)