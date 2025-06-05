with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt") as tsla_file:
    lines = tsla_file.read().split()

prices = [round(float(line),2) for line in lines]

day1of3 = 0
day2of3 = 1
day3of3 = 2





print(prices)






