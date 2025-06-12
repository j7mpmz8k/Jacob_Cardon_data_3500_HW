import json


def import_stock(file_name):
    directory_path = "/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw5/"
    with open(directory_path+file_name) as stock_file: #mar18,2024 - mar17,2025....matching example given in HW4
        lines = stock_file.read().split()# converts to a list
        lines = [round(float(line),2) for line in lines]# sets each price value to a float rounded to two decimal places
    ticker = find_ticker(file_name)
    return lines


#calculates previous 5 day moving average along with error preventions ensuring 5 days are available to calculate
def last_5day_avg_from(stock_prices, day=0):
    day5 = day
    day1 = day-5
    if day1 < 0:
        return print("\nERROR! Day must be no less than 5, and no more than", len(stock_prices), "\n")
    return sum(stock_prices[day1:day5])/5


def meanReversionStrategey(ticker, stock_prices):
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print("\n"+ticker,"Mean Reversion Strategy Output: Mar18,2024 - Mar17,2025")
    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(stock_prices):# keeps track of index position of each day and price value
        if day > 5:# ensures at least 5 days have past till 5day average calculates

            #ensures today's price is at least 2% less than last 5 day moving avg
            #AND not to double up on stock inventory
            if price > last_5day_avg_from(stock_prices, day)*1.02 and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                print("sell at:\t$",price)
                print("trade profits:\t$",trade_profits)
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last 5 day moving avg
            # AND not to double up on stock inventory
            elif price < last_5day_avg_from(stock_prices, day)*0.98 and buy == 0:#buy conditions
                print("\nbuy at:\t\t$",price)
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    final_profit_percentage = str(round((total_profit/first_buy)*100,2))+"%"
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print("-"*24)#creates a line for formatting
    print("total profits:\t"+"$",total_profit)
    print("first buy:\t"+"$",first_buy)
    print("percent return:\t",final_profit_percentage,"\n")
    return stock_prices, total_profit, final_profit_percentage


def simpleMovingAverageStrategy(ticker, stock_prices):
    #initialization for transaction history analytics
    total_profit = 0
    buy = 0
    first_buy = 0

    print("\n"+ticker,"Simple Moving Average Strategy Output: Mar18,2024 - Mar17,2025")
    #calculates buy/sell conditions and individual trade profits
    for day, price in enumerate(stock_prices):# keeps track of index position of each day and price value
        if day > 5:# ensures at least 5 days have past till 5day average calculates

            #ensures today's price is at least 2% less than last 5 day moving avg
            #AND not to double up on stock inventory
            if price > last_5day_avg_from(stock_prices, day) and buy != 0:#sell conditions
                trade_profits = round(price - buy,2)#initiates purchase of stock
                total_profit += trade_profits#adds to total profits
                print("sell at:\t$",price)
                print("trade profits:\t$",trade_profits)
                if first_buy == 0:
                    first_buy = buy# keeps track of price of first purchase for return on investment
                buy = 0# resets stock inventory to zero

            #ensures today's price is at least 2% greater than last 5 day moving avg
            # AND not to double up on stock inventory
            elif price < last_5day_avg_from(stock_prices, day) and buy == 0:#buy conditions
                print("\nbuy at:\t\t$",price)
                buy = price# updates stock inventory to current purchase

    #calculates ROI % 
    final_profit_percentage = str(round((total_profit/first_buy)*100,2))+"%"
    total_profit = round(total_profit,2)

    #prints final totals of profits and returns of a year of trade history         
    print("-"*24)#creates a line for formatting
    print("total profits:\t"+"$",total_profit)
    print("first buy:\t"+"$",first_buy)
    print("percent return:\t",final_profit_percentage,"\n")
    return stock_prices, total_profit, final_profit_percentage

def find_ticker(file):
    ticker = ""
    for char in file:
        if char == ".":
            break
        ticker += char
    return ticker

returns = {}
def send_to_json(ticker, stock_prices):
    prices, mr_profit, mr_returns = meanReversionStrategey(ticker, stock_prices)
    prices, sma_profit, sma_returns = simpleMovingAverageStrategy(ticker, stock_prices)
    returns[ticker+"_prices"] = prices
    returns[ticker+"_mr_profit"] = mr_profit
    returns[ticker+"_mr_returns"] = mr_returns
    returns[ticker+"_sma_profit"] = sma_profit
    returns[ticker+"_sma_returns"] = sma_returns

#----------------------------------------------------------------------------------------------------

# 1. Create a list of all your stock filenames
stock_files = ["AAPL.txt", "META.txt", "AMZN.txt", "COIN.txt", "GOOG.txt", "HOOD.txt", "NVDA.txt", "TSLA.txt", "VOO.txt"]

for file_name in stock_files:
    ticker = find_ticker(file_name)
    prices = import_stock(file_name)
    send_to_json(ticker, prices)

with open("stock_analysis_results.json", "w") as f:
    json.dump(returns, f, indent=1)