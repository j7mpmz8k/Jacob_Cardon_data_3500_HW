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

#######################################################################################################################

#calculates previous "N_days" moving average along with error preventions ensuring "N_days" are available to calculate
#pulls price data passed down from functions
def calculate_Nday_avg(prices, N_days, day=0):
    dayN = day
    day1 = day-N_days
    if day1 < 0:
        return print(f'\nERROR! Day must be no less than {N_days} and no more than {len(prices)} \n')
    return sum(prices[day1:dayN])/N_days

def calculate_ema(data, period):
    """
    Calculates the Exponential Moving Average (EMA) for a given list of data.

    Args:
        data (list of float): A list of numerical data (e.g., closing prices).
        period (int): The period for the EMA calculation.

    Returns:
        list of float: A list containing the EMA values. Returns an empty list
                       if the data is insufficient for the period.
    """
    if len(data) < period:
        return []

    ema_values = []
    # The multiplier for smoothing.
    multiplier = 2 / (period + 1)
    
    # The first EMA is a simple moving average of the first 'period' prices.
    sma = sum(data[:period]) / period
    ema_values.append(sma)

    # Calculate the subsequent EMA values
    for i in range(period, len(data)):
        current_price = data[i]
        previous_ema = ema_values[-1]
        current_ema = (current_price - previous_ema) * multiplier + previous_ema
        ema_values.append(current_ema)
        
    return ema_values

def calculate_macd(close_prices, day, short_period=12, long_period=26, signal_period=9):
    """
    Calculates the MACD line, Signal line, and Histogram.

    Args:
        close_prices (list of float): A list of closing prices.
        short_period (int): The period for the short-term EMA (default 12).
        long_period (int): The period for the long-term EMA (default 26).
        signal_period (int): The period for the Signal line EMA (default 9).

    Returns:
        tuple: A tuple containing three lists (macd_line, signal_line, histogram).
               Returns ([], [], []) if the data is insufficient.
    """
    if len(close_prices) < long_period:
        print("Not enough data to calculate MACD.")
        return [], [], []

    # Calculate the 12-period and 26-period EMAs
    ema_short = calculate_ema(close_prices, short_period)
    ema_long = calculate_ema(close_prices, long_period)

    # The MACD calculation can only start where both EMAs are available.
    # The longer EMA starts later, so we align our MACD calculation to its start.
    alignment_offset = long_period - short_period
    
    # Calculate the MACD line
    macd_line = []
    for i in range(len(ema_long)):
        # Align the short EMA with the long EMA
        macd_value = ema_short[i + alignment_offset] - ema_long[i]
        macd_line.append(macd_value)

    # Calculate the Signal line (9-period EMA of the MACD line)
    signal_line = calculate_ema(macd_line, signal_period)

    # Calculate the Histogram
    # The histogram can only be calculated where the signal line is available.
    histogram_offset = signal_period - 1
    histogram = []
    for i in range(len(signal_line)):
      # Align the MACD line with the Signal line
      histogram_value = macd_line[i + histogram_offset] - signal_line[i]
      histogram.append(round(histogram_value,4))

    # To ensure all lists are the same length for easy plotting,
    # we trim the beginning of the macd_line and signal_line.
    final_macd_line = macd_line[histogram_offset:]

    start_day = len(prices) - len(histogram)
    index_of_histogram = day-start_day
    if day >= start_day:
        return histogram[index_of_histogram]
    else:
        return None


###########################################################################################


# calculates & prints trading strategy with at 2% difference from "N_days" moving average
def meanReversionStrategey(ticker, prices, N_days=200):
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} {N_days}day Mean Reversion Strategy Over Period of: {len(prices)} days')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day >= N_days:# ensures at least "N_days" have past till "N_days" average calculates

            #ensures today's price is at least 2% less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price > calculate_Nday_avg(prices, N_days, day)*1.02 and buy != 0:#sell conditions
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
            elif price < calculate_Nday_avg(prices, N_days, day)*0.98 and buy == 0:#buy conditions
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
def BollingerBandsStrategy(ticker, prices, N_days=200):

    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} {N_days}day Simple Moving Average Strategy Output Over Period of: {len(prices)} days')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day >= N_days:# ensures at least "N_days" days have past till "N_days" average calculates

            #ensures today's price is less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price < calculate_Nday_avg(prices, N_days, day)*.95 and buy != 0:#sell conditions
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
            elif price > calculate_Nday_avg(prices, N_days, day)*1.05 and buy == 0:#buy conditions
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

def MacdStrategey(ticker, prices):
    N_days = 200# executes strategy over Nth number of days
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('-'*44)#creates a line for formatting
    print(f'{ticker} Macd Strategy Over Period of: {len(prices)} days')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if calculate_macd(prices, day) is None:# ensures at least "N_days" have past till "N_days" average calculates
            pass
        else:

            #ensures today's price is at least 2% less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if calculate_macd(prices, day) < 0 and buy != 0:#sell conditions
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
            elif calculate_macd(prices, day) > 0 and buy == 0:#buy conditions
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
    bb_profit, bb_returns = BollingerBandsStrategy(ticker, prices)
    macd_profit, macd_returns = MacdStrategey(ticker, prices)
    returns[f'{ticker}_mr_profit'] = mr_profit
    returns[f'{ticker}_mr_returns'] = mr_returns
    returns[f'{ticker}_bb_profit'] = bb_profit
    returns[f'{ticker}_bb_returns'] = bb_returns
    returns[f'{ticker}_macd_profit'] = macd_profit
    returns[f'{ticker}_macd_returns'] = macd_returns

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