file = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt")
file_lines = file.readlines()
complete_price_list = []

#converting list to a list of floats
for stock_price_local in file_lines:
    stock_price_local = float(stock_price_local)
    complete_price_list.append(stock_price_local)

print(complete_price_list)