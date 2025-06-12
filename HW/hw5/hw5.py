import json
directory_path = '/home/Ubuntu/Jacob_Cardon_data_3500_HW/HW/hw5/'#used for both read and write directory
stock_files = ['AAPL.txt', 'ADBE.txt', 'META.txt', 'AMZN.txt', 'COIN.txt', 'GOOG.txt', 'HOOD.txt', 'NVDA.txt', 'TSLA.txt', 'VOO.txt']
date_range = "12Jun24-11Jun25"# one year of data for files pre-sorted with oldest at the top, newest at the bottom

# used inside "import_stock" function to extract ticker from file name
def find_ticker(file_name):
    ticker = ''
    for char in file_name:
        if char == '.':
            break
        ticker += char
    return ticker

#reads all files from "stock_files" variable. 
#Returns ticker and prices to be passed into trading stratagy calculation functions along with functions to save to dictionary and .json file
def import_stock(file_name):
    with open(directory_path+file_name) as stock_file:
        lines = stock_file.read().split()# converts to a list
        prices = [round(float(line),2) for line in lines]# sets each price value to a float rounded to two decimal places
    ticker = find_ticker(file_name)
    return ticker, prices

''' Abstraction layers of "ticker" and "prices" returned
"prices" -->import_stock-->send_to_dictionary-->(meanReversionStrategey or simpleMovingAverageStrategy-->last_N_day_avg_from)-->send_to_dictionary
"ticker" -->(import_stock-->find_ticker)-->send_to_dictionary-->meanReversionStrategey or simpleMovingAverageStrategy-->send_to_dictionary
'''

#calculates previous 5 day moving average along with error preventions ensuring 5 days are available to calculate
#pulls price data passed down from functions
def last_N_day_avg_from(prices, N_days, day=0):
    dayN = day
    day1 = day-N_days
    if day1 < 0:
        return print('\nERROR! Day must be no less than', N_days, 'and no more than', len(prices), '\n')
    return sum(prices[day1:dayN])/N_days


# calculates & prints trading stratagy with at 2% difference from "N_days" moving average
def meanReversionStrategey(ticker, prices):
    N_days = 5# executes strategy over Nth number of days
    
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('\n'+ticker,'Mean Reversion Strategy Output:', date_range)
    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day > N_days:# ensures at least "N_days" have past till 5day average calculates

            #ensures today's price is at least 2% less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price > last_N_day_avg_from(prices, N_days, day)*1.02 and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                print('sell at:\t$',price)
                print('trade profits:\t$',trade_profits)
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price < last_N_day_avg_from(prices, N_days, day)*0.98 and buy == 0:#buy conditions
                print('\nbuy at:\t\t$',price)
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    final_profit_percentage = str(round((total_profit/first_buy)*100,2))+'%'
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print('-'*24)#creates a line for formatting
    print('total profits:\t'+'$',total_profit)
    print('first buy:\t'+'$',first_buy)
    print('percent return:\t',final_profit_percentage,'\n')
    return prices, total_profit, final_profit_percentage

# calculates & prints trading stratagy with any difference from "N_days" moving average inversed from meanReversionStrategey
def simpleMovingAverageStrategy(ticker, prices):
    N_days = 50# executes strategy over Nth number of days

    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print('\n'+ticker,'Simple Moving Average Strategy Output:',date_range)
    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(prices):# keeps track of index position of each day and price value
        if day > N_days:# ensures at least "N_days" days have past till 5day average calculates

            #ensures today's price is less than last "N_days" moving avg
            #AND not to double up on stock inventory
            if price < last_N_day_avg_from(prices, N_days, day) and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                print('sell at:\t$',price)
                print('trade profits:\t$',trade_profits)
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is greater than last "N_days" moving avg
            # AND not to double up on stock inventory
            elif price > last_N_day_avg_from(prices, N_days, day) and buy == 0:#buy conditions
                print('\nbuy at:\t\t$',price)
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    final_profit_percentage = str(round((total_profit/first_buy)*100,2))+'%'
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print('-'*24)#creates a line for formatting
    print('total profits:\t'+'$',total_profit)
    print('first buy:\t'+'$',first_buy)
    print('percent return:\t',final_profit_percentage,'\n')
    return prices, total_profit, final_profit_percentage

#sets up dictionary of trading analysis preperatory to exporting to .json
#also exucutes calculations of trading stratagies
returns = {}
def send_to_dictonary(ticker, prices):
    prices, mr_profit, mr_returns = meanReversionStrategey(ticker, prices)
    prices, sma_profit, sma_returns = simpleMovingAverageStrategy(ticker, prices)
    returns[ticker+'_prices'] = prices
    returns[ticker+'_mr_profit'] = mr_profit
    returns[ticker+'_mr_returns'] = mr_returns
    returns[ticker+'_sma_profit'] = sma_profit
    returns[ticker+'_sma_returns'] = sma_returns

#exports dictionary to .json file
def saveResults(dictionary):
    with open(directory_path+'results.json', 'w') as file:
        json.dump(dictionary, file, indent=4)
    print('\n"results.json" saved to:', directory_path, '\n')

#----------------------------------------------------------------------------------------------------

# execution script to open, read, perform anaylis, and save to dictionary
for file_name in stock_files:
    ticker, prices = import_stock(file_name)# finds files from directory variable, reads data and extracts ticker from file name and price data within file
    send_to_dictonary(ticker, prices)# caluclates trading strading stratagies and saves analysis to dictionary

#writes saved dictionary to results.json file to directory path variable
saveResults(returns)