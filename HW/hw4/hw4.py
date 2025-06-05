import numpy as np

header = np.array(['Date','Close/Last','Volume','Open','High','Low'])
date_col = 0
closing_col = 1
volume_col = 2
opening_col = 3
high_col = 4
low_col = 5


with open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.csv") as tsla_file:
    lines = tsla_file.read().split()

stock_price_2D = np.array([line.split(",") for line in lines][1:][::-1])

def col_in_day(col,day):
    return col[day[stock_price_2D]]



print(header,stock_price_2D,sep="\n")


