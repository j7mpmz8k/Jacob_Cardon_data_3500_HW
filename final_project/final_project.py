import json
import requests
import time
directory_path = '/home/crostini/Github/Jacob_Cardon_data_3500_HW/final_project/'
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

def import_stock(ticker):
    """reads all files from "stock_files" variable. 
    Returns ticker and prices to be passed into trading strategy calculation functions along with functions to save to dictionary and .json file"""
    req = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey=KSH53YGYAHBD4J02')
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

    #tries to update and append data from api
    try:
        with open(f'{directory_path}{ticker}.csv', 'r') as csv_file:
            lines = csv_file.readlines()
            last_date = lines[-1].split(',')[0]
        new_lines = []

        #pulls all close prices and all dates
        for date_key in raw_data[key1]:
            if date_key > last_date:
                new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
        new_lines.reverse()

        with open(f'{directory_path}{ticker}.csv', 'a') as csv_file:
            csv_file.writelines(new_lines)
        print('found existing file, appending new data')
    #if file is empty or does not exist, file is recreated
    except (FileNotFoundError, IndexError):
        print('\nERROR! file not found or file is empty. Recreating file.')
        new_lines = []
        #pulls all close prices in all dates
        for date_key in raw_data[key1]:
            new_lines.append(f'{date_key},{round(float(raw_data[key1][date_key][key3_close]),2)}\n')
        new_lines.reverse()

        #writes extracted data to a csv file for each stock
        with open(f'{directory_path}{ticker}.csv', 'w') as csv_file:
            csv_file.writelines(new_lines)

    #reads newly refreshed data for analysis
    with open(f'{directory_path}{ticker}.csv', 'r') as csv_file:
        lines = csv_file.readlines()
        prices = []
        for line in lines:
            prices.append(float(line.split(',')[-1].strip()))
    return prices

#######################################################################################################################


def calculate_Nday_avg(prices, N_days, day=0):
    """calculates previous "N_days" moving average along with error preventions ensuring "N_days" are available to calculate
    pulls price data passed down from functions"""
    dayN = day
    day1 = day-N_days
    if day1 < 0:
        return print(f'\nERROR! Day must be no less than {N_days} and no more than {len(prices)} \n')
    return sum(prices[day1:dayN])/N_days

def calculate_ema(prices, period):
    if len(prices) < period:#ensures minimum price history has passed
        return []
    # The multiplier for smoothing.
    multiplier = 2 / (period + 1)
    sma = sum(prices[:period]) / period
    ema_values = [sma]#first ema value is sma acting as a starting point for future ema calculations

    #creates a stored list of ema values corresponding to each day of each closing price
    for i in range(period, len(prices)):
        current_ema = (prices[i] * multiplier) + (ema_values[-1] * (1 - multiplier))
        ema_values.append(current_ema)

    return ema_values


def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    ''' macd is is a calculation dirived from (shortEMA - longEMA = the macd line)
    the buy/sell signal is the (macd line - signalEMA = histogram)
    when histogram is negative, it signals a downtrend signaling to sell
    when histogram is positive, it signals an uptrend signaling to buy'''

    # Ensures there's enough data for a single MACD value to be calculated
    if len(prices) < long_period + signal_period:
        print("Insufficent price history")
        return []

    # Calculates long/short ema...a list of daily long/short ema values are returned
    ema_short = calculate_ema(prices, short_period)
    ema_long = calculate_ema(prices, long_period)

    # compensates for minimum price history required to calculate short vs long EMA
    alignment_offset = long_period - short_period
    
    # macd line = shortEMA - longEMA
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
    
    #histogram = macd - signalEMA
    histogram = []
    for i in range(len(signal_line)):
      histogram_value = macd_for_histogram[i] - signal_line[i]
      histogram.append(round(histogram_value, 4))

    return histogram #outputs list of daily historgram data.


###########################################################################################


def MeanReversionStrategey(ticker, prices, N_days=200):
    """calculates & prints trading strategy with at 2% difference from "N_days" moving average"""
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action# tells user if they should buy or sell, prints message at end

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

    #check if stock is most profitable in strategy, updates if most profitable
    if total_profit > most_profitable['MR_strat']['total_profit']:
        most_profitable['MR_strat']['total_profit'] = total_profit
        most_profitable['MR_strat']['ticker'] = ticker
    #prints final totals of profits and returns of a year of trade history
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}') 
    return total_profit, final_profit_percentage

def BollingerBandsStrategy(ticker, prices, N_days=200):
    """calculates & prints trading strategy with any difference from "N_days" moving average*5% inverted from MeanReversionStrategey"""

    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action# tells user if they should buy or sell, prints message at end

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

    #check if stock is most profitable in strategy, updates if most profitable
    if total_profit > most_profitable['BB_strat']['total_profit']:
        most_profitable['BB_strat']['total_profit'] = total_profit
        most_profitable['BB_strat']['ticker'] = ticker

    #prints final totals of profits and returns of a year of trade history
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}') 
    return total_profit, final_profit_percentage

def MacdStrategey(ticker, prices):
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0
    global today_action# tells user if they should buy or sell, prints message at end

    print('-'*60)
    print(f'{ticker} Macd Strategy Over Period of: {len(prices)} days')

    #returns the Histogram buy/sell values from after calculating macd line - signalEMA
    histogram = calculate_macd(prices)
    #If the histogram is empty, ussually due to less than 35 days... 26days from(longEMA) +9days from (signalEMA)= 35 days minimum
    if len(histogram) == 0:
        print("Error! Insufficient price data.")
        print(f'total profits:\t$ 0.00')
        print(f'first buy:\t$ 0.00')
        print(f'percent return:\t  0.00%')
        print('-'*60)
        return 0, "0.00%"# returns zero profits and zero returns if histogram data is empty

    #histogram data requires minimum time passed, can't start from first day(0), offset aligns the index's
    start_day_offset = len(prices) - len(histogram)

    # calculates trading from histogram data, negative=sell positive=buy
    for i in range(len(histogram)):
        alligned_price_day_index = start_day_offset+i#ensures that the first day of histogram index is aligned with index of price day
        price = prices[alligned_price_day_index]#finds price corresponding to same day of histogram day
        hist_value = histogram[i]

        # Sell condition: histogram falls negative
        if hist_value < 0 and buy != 0:
            trade_profits = round(price - buy, 2)
            total_profit += trade_profits
            if alligned_price_day_index == len(prices)-1: # Check if it is the most recent day
                today_action += f'ACTION! Today you should sell {ticker} at: ${price}\n'
            if first_buy == 0:# checks if inventory is zero, avoids buying more than 1
                first_buy = buy
            buy = 0 # Stock sold

        # Buy condition: histogram becomes positive
        elif hist_value > 0 and buy == 0:
            if alligned_price_day_index == len(prices)-1: # Check if it is the most recent day
                today_action += f'ACTION! Today you should buy {ticker} at: ${price}\n'
            buy = price # Stock bought at current price in loop

    #calculates ROI % 
    try:
        final_profit_percentage = f'{round((total_profit / first_buy) * 100, 2)}%'
    except ZeroDivisionError:
        final_profit_percentage = "0.00%"
    total_profit = round(total_profit, 2)

    #check if stock is most profitable in strategy, updates if most profitable
    if total_profit > most_profitable['MACD_strat']['total_profit']:
        most_profitable['MACD_strat']['total_profit'] = total_profit
        most_profitable['MACD_strat']['ticker'] = ticker
    
    print(f'total profits:\t$ {total_profit}')
    print(f'first buy:\t$ {first_buy}')
    print(f'percent return:\t  {final_profit_percentage}')
    print('-'*60)
    return total_profit, final_profit_percentage


def analyze_stocks(ticker, prices):
    """executes calculations of trading strategies, adds to results dictionary"""
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


def saveResults(dictionary):
    """exports dictionary to .json file"""
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
print(today_action)# tells user if current day is a buy or sell signal for each stock

#reveals most profitable stocks for each strategy for lifetime of price history
print('Most lifetime profitable stock/strategies:')
print(f'\tMean Reversion(200dayAVG):\t\t\t\t{most_profitable["MR_strat"]['ticker']} total profit @ ${most_profitable["MR_strat"]['total_profit']}')
print(f'\tBollinger Bands(200dayAVG):\t\t\t\t{most_profitable["BB_strat"]['ticker']} total profit @ ${most_profitable["BB_strat"]['total_profit']}')
print(f'\tMACD(shortEMA=12day longEMA=26day signalEMA-9day):\t{most_profitable["MACD_strat"]['ticker']} total profit @ ${most_profitable["MACD_strat"]['total_profit']}')


#writes saved dictionary to results.json file to directory path variable
saveResults(results)