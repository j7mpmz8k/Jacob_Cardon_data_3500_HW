with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt") as tsla_file: #mar18,2024 - mar17,2025....matching example given in HW4
    lines = tsla_file.read().split()

prices = [round(float(line),2) for line in lines]


#calculates previous 5 day moving average along with calculation error preventions from less than 5 days available to calculate
def last_5day_avg_from(day=0):
    day5 = day
    day1 = day-5
    if day1 < 0:
        return print("\nERROR! Day must be no less than 5, and no more than", len(prices), "\n")
    return sum(prices[day1:day5])/5


total_profit = 0
buy = 0
first_buy = 0


for day, price in enumerate(prices):
    if day > 5:
        if price > last_5day_avg_from(day)*1.02 and buy != 0:
            trade_profits = round(price - buy,2)
            total_profit += trade_profits
            print("sell at:\t$",price)
            print("trade profits:\t$",trade_profits)
            if first_buy == 0:
                first_buy = buy
            buy = 0
        elif price < last_5day_avg_from(day)*0.98 and buy == 0:
            print("\nbuy at:\t\t$",price)
            buy = price

#prints final totals of profits and returns relative to             
print("-"*24)
print("total profits:\t"+"$",round(total_profit,2))
print("first buy:\t"+"$",first_buy)
print("percent return:\t"+"%",round((total_profit/first_buy)*100,2),"\n")