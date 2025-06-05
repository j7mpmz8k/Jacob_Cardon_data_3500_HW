with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt") as tsla_file:
    lines = tsla_file.read().split()

prices = [round(float(line),2) for line in lines]

def last_5day_avg_from(day=0):
    day5 = day
    day1 = day-5
    if day1 < 0:# or day > len(prices):
        return print("\nERROR! Day must be no less than 5, and no more than", len(prices), "\n")
    return sum(prices[day1:day5])/5


total_profit = 0
buy = 0
first_buy = 0
for day, price in enumerate(prices):
    if day < 6:
        None
    else:
        if price > last_5day_avg_from(day)*1.02 and buy != 0:
            trade_profits = round(price - buy,2)
            total_profit += trade_profits
            print("day:",day+1, "sell at", "$"+str(price))
            print("trade profits:", "$"+str(trade_profits), "\n")
            if first_buy == 0:
                first_buy = buy
            buy = 0
        elif price < last_5day_avg_from(day)*0.98 and buy == 0:
            print("day:",day+1, "buy at", "$"+str(price))
            buy = price
print("-"*20,end="\n")
print("total profits", "$"+str(total_profit))
print("first buy", "$"+str(first_buy))
print("percent return:", "%"+str(round((total_profit/first_buy)*100,2)))