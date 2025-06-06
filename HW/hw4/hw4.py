with open("/home/ubuntu/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt") as tsla_file: #mar18,2024 - mar17,2025....matching example given in HW4
    lines = tsla_file.read().split()# converts to a list

# sets each price value to a float rounded to two decimal places
prices = [round(float(line),2) for line in lines]


#calculates previous 5 day moving average along with error preventions ensuring 5 days are available to calculate
def last_5day_avg_from(day=0):
    day5 = day
    day1 = day-5
    if day1 < 0:
        return print("\nERROR! Day must be no less than 5, and no more than", len(prices), "\n")
    return sum(prices[day1:day5])/5


#initialization for transaction history analytics
total_profit = 0
buy = 0
first_buy = 0

print("\nTSLA Mean Reversion Strategy Output: Mar18,2024 - Mar17,2025")
#calculates buy/sell conditions and individual trade profits
for day, price in enumerate(prices):# keeps track of index position of each day and price value
    if day > 5:# ensures at least 5 days have past till 5day average calculates

        #ensures today's price is at least 2% less than last 5 day moving avg
        #AND not to double up on stock inventory
        if price > last_5day_avg_from(day)*1.02 and buy != 0:#sell conditions
            trade_profits = round(price - buy,2)#initiates purchase of stock
            total_profit += trade_profits#adds to total profits
            print("sell at:\t$",price)
            print("trade profits:\t$",trade_profits)
            if first_buy == 0:
                first_buy = buy# keeps track of price of first purchase for return on investment
            buy = 0# resets stock inventory to zero

        #ensures today's price is at least 2% greater than last 5 day moving avg
        # AND not to double up on stock inventory
        elif price < last_5day_avg_from(day)*0.98 and buy == 0:#buy conditions
            print("\nbuy at:\t\t$",price)
            buy = price# updates stock inventory to current purchase

#calculates ROI % 
final_profit_percentage = round((total_profit/first_buy)*100,2)

#prints final totals of profits and returns of a year of trade history         
print("-"*24)#creates a line for formatting
print("total profits:\t"+"$",round(total_profit,2))
print("first buy:\t"+"$",first_buy)
print("percent return:\t",str(final_profit_percentage)+"%","\n")