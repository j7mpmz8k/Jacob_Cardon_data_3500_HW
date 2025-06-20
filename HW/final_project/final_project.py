import json
import requests
import time
directory_path = '/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/final_project/'
tickers = ['AAPL', 'ADBE', 'META', 'AMZN', 'COIN', 'GOOG', 'HOOD', 'NVDA', 'TSLA', 'VOO']
today_action = ''
most_profitable = {
'MR_strat':{'ticker':'','total_profit':0},
'BB_strat':{'ticker':'','total_profit':0},
'MACD_strat':{'ticker':'','total_profit':0}
}

#sets up dictionary of trading analysis preparatory to exporting to .json
results = {
'today_action':'',
"Most Profitable":{},
'analysis':{},
}

#reads all files from "stock_files" variable. 
#Returns ticker and prices to be passed into trading strategy calculation functions along with functions to save to dictionary and .json file
def import_stock(ticker):
    req = requests.get(f'http://www.multipliervantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey=NG9C9EPVYBMQT0C8')
    time.sleep(12)
    raw_data = json.loads(req.text)#.loads() used instead of .load() since json dictionary is contained within a string
    #listing out available keys
    key1 = 'Time Series (Daily)'
    key2_date = '2025-06-16'# Note! many more dates
    key3_open = '1. open'
    key3_high = '2. high'
    key3_low = '3. low'
    key3_close = '4. close'
    key3_volume = '5. volume'

    try:
        with open(f'{directory_path}{ticker}.csv', 'r') as csv_file:
            lines = csv_file.readlines()
            last_date = lines[-1].split(',')[0]
        new_lines = []

        #pulls all close prices in all dates
        for date_key in raw_data[key1]:
            if date_key > last_date:
                new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_volume]),2)},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
        new_lines.reverse()

        with open(f'{directory_path}{ticker}.csv', 'a') as csv_file:
            csv_file.writelines(new_lines)
        print('found existing file, appending new data')
    except (FileNotFoundError, IndexError):
        print('\nERROR! file not found or file is empty. Recreating file.')
        new_lines = []
        #pulls all close prices in all dates
        for date_key in raw_data[key1]:
            new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_volume]),2)},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
        new_lines.reverse()

        with open(f'{directory_path}{ticker}.csv', 'w') as csv_file:
            csv_file.writelines(new_lines)

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

def calculate_ema(prices, period):
    if len(prices) < period:
        return []

    # The multiplier for smoothing.
    multiplier = 2 / (period + 1)
    
    # The first EMA is a simple moving average of the first 'period' prices.
    sma = sum(prices[:period]) / period
    ema_values = [sma]

    for i in range(period, len(prices)):
        current_ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
        ema_values.append(current_ema)
        
    return ema_values

def calculate_macd_series(prices, short_period=12, long_period=26, signal_period=9):
    # Ensure there's enough data for a single MACD value to be calculated
    if len(prices) < long_period + signal_period:
        print("Insufficent price history")
        return []

    # Calculate the 12-period and 26-period EMAs
    ema_short = calculate_ema(prices, short_period)
    ema_long = calculate_ema(prices, long_period)

    # Align the shorter EMA with the longer one to calculate the MACD line
    alignment_offset = long_period - short_period
    
    macd_line = []
    for i in range(len(ema_long)):
        macd_value = ema_short[i + alignment_offset] - ema_long[i]
        macd_line.append(macd_value)

    # Calculate the Signal line (9-period EMA of the MACD line)
    if len(macd_line) < signal_period:
        return [] # Not enough MACD data to create a signal line
    signal_line = calculate_ema(macd_line, signal_period)

    # Align the MACD line with the Signal line to calculate the histogram
    # The signal line is shorter, so we trim the start of the macd_line to match
    macd_for_histogram = macd_line[len(macd_line) - len(signal_line):]
    
    histogram = []
    for i in range(len(signal_line)):
      histogram_value = macd_for_histogram[i] - signal_line[i]
      histogram.append(round(histogram_value, 4))

    # Return the three lists, which are now all aligned and the same length
    return histogram


###########################################################################################


# calculates & prints trading strategy with at 2% difference from "N_days" moving average
def MeanReversionStrategey(ticker, prices, N_days=200):
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action

    print('-'*60)#creates a line for formatting
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
                    today_action += f'ACTION! Today you should sell {ticker} at: ${price}\n'
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price < calculate_Nday_avg(prices, N_days, day)*0.98 and buy == 0:#buy conditions
                if day == len(prices)-1:# checks if day is most recent day
                    today_action += f'ACTION! Today you should buy {ticker} at: ${price}\n'
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit/first_buy)*100,2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit,2)

    if total_profit > most_profitable['MR_strat']['total_profit']:
        most_profitable['MR_strat']['total_profit'] = total_profit
        most_profitable['MR_strat']['ticker'] = ticker
    #prints final totals of profits and returns of a year of trade history
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}') 
    return total_profit, final_profit_percentage

# calculates & prints trading strategy with any difference from "N_days" moving average inverted from MeanReversionStrategey
def BollingerBandsStrategy(ticker, prices, N_days=200):

    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action

    print('-'*60)#creates a line for formatting
    print(f'{ticker} {N_days}day Bollinger Bands Strategy Over Period of: {len(prices)} days')

    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day >= N_days:# ensures at least "N_days" days have past till "N_days" average calculates

            #ensures today's price is less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price < calculate_Nday_avg(prices, N_days, day)*.95 and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                if day == len(prices)-1:# checks if day is most recent day
                    today_action += f'ACTION! Today you should sell {ticker} at: ${price}\n'
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price > calculate_Nday_avg(prices, N_days, day)*1.05 and buy == 0:#buy conditions
                if day == len(prices)-1:# checks if day is most recent day
                    today_action += f'ACTION! Today you should buy {ticker} at: ${price}\n'
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit/first_buy)*100,2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit,2)

    if total_profit > most_profitable['BB_strat']['total_profit']:
        most_profitable['BB_strat']['total_profit'] = total_profit
        most_profitable['BB_strat']['ticker'] = ticker

    #prints final totals of profits and returns of a year of trade history
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}') 
    return total_profit, final_profit_percentage

def MacdStrategey(ticker, prices):
    """
    Calculates and prints a trading strategy based on the MACD indicator.
    
    This function is optimized to calculate the MACD series once, preventing
    performance issues on large datasets.
    """
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action

    print('-'*60)
    print(f'{ticker} Macd Strategy Over Period of: {len(prices)} days')

    # --- PERFORMANCE FIX ---
    # 1. Calculate the MACD, Signal, and Histogram series ONCE before the loop.
    histogram = calculate_macd_series(prices)

    # 2. If the histogram is empty, it means there wasn't enough data. Exit early.
    if not histogram:
        print("Could not perform MACD strategy due to insufficient price data.")
        print(f'total profits:\t$ 0.00')
        print(f'first buy:\t$ 0.00')
        print(f'percent return:\t  0.00%')
        print('-'*60)
        return 0, "0.00%"

    # 3. Determine the starting day for our strategy. The MACD data doesn't
    #    exist for the early days, so we offset our loop to where it starts.
    start_day_offset = len(prices) - len(histogram)

    # 4. Loop through the pre-calculated histogram data.
    for i in range(len(histogram)):
        current_day_in_prices = start_day_offset+i
        price = prices[current_day_in_prices]
        hist_value = histogram[i]

        # Sell condition: histogram crosses below zero and we own the stock
        if hist_value < 0 and buy != 0:
            trade_profits = round(price - buy, 2)
            total_profit += trade_profits
            if current_day_in_prices == len(prices)-1: # Check if it is the most recent day
                today_action += f'ACTION! Today you should sell {ticker} at: ${price}\n'
            if first_buy == 0:
                first_buy = buy
            buy = 0 # Stock sold

        # Buy condition: histogram crosses above zero and we don't own the stock
        elif hist_value > 0 and buy == 0:
            if current_day_in_prices == len(prices)-1: # Check if it is the most recent day
                today_action += f'ACTION! Today you should buy {ticker} at: ${price}\n'
            buy = price # Stock bought

    # ROI and final printout logic (remains the same)
    try:
        final_profit_percentage = f'{round((total_profit / first_buy) * 100, 2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit, 2)

    if total_profit > most_profitable['MACD_strat']['total_profit']:
        most_profitable['MACD_strat']['total_profit'] = total_profit
        most_profitable['MACD_strat']['ticker'] = ticker

    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}')
    print('-'*60)
    return total_profit, final_profit_percentage


# executes calculations of trading strategies
def analyze_stocks(ticker, prices):
    results['analysis'][f'{ticker}_prices'] = prices
    mr_profit, mr_returns = MeanReversionStrategey(ticker, prices)
    bb_profit, bb_returns = BollingerBandsStrategy(ticker, prices)
    macd_profit, macd_returns = MacdStrategey(ticker, prices)
    results['analysis'][f'{ticker}_mr_profit'] = mr_profit
    results['analysis'][f'{ticker}_mr_returns'] = mr_returns
    results['analysis'][f'{ticker}_bb_profit'] = bb_profit
    results['analysis'][f'{ticker}_bb_returns'] = bb_returns
    results['analysis'][f'{ticker}_macd_profit'] = macd_profit
    results['analysis'][f'{ticker}_macd_returns'] = macd_returns

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
results["Most Profitable"] = most_profitable
results['today_action'] = today_action

print('-'*60)
print(today_action)

print('Most profitable stock/strategies:')
print(f'\tMean Reversion(200day):\t\t\t\t{most_profitable["MR_strat"]['ticker']} total profit @ ${most_profitable["MR_strat"]['total_profit']}')
print(f'\tBollinger Bands(200day):\t\t\t{most_profitable["BB_strat"]['ticker']} total profit @ ${most_profitable["BB_strat"]['total_profit']}')
print(f'\tMACD(short-12day long-26day signal-9day):\t{most_profitable["MACD_strat"]['ticker']} total profit @ ${most_profitable["MACD_strat"]['total_profit']}')


#writes saved dictionary to results.json file to directory path variable
saveResults(results)