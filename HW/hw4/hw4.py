with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt") as tsla_file:
    lines = tsla_file.read().split()

prices = [round(float(line),2) for line in lines]

def last_5day_avg_from(day=0):
    day5 = day
    day1 = day-5
    if day1 < 0 or day5 > len(prices):
        return print("\nERROR! Day must be no less than 5, and no more than", len(prices), "\n")
    return sum(prices[day1:day5])/5,prices[day1:day5]

print(last_5day_avg_from())