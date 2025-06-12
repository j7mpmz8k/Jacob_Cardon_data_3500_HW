def import_stock(file_path):
    with open(file_path) as stock_file: #mar18,2024 - mar17,2025....matching example given in HW4
        lines = stock_file.read().split()# converts to a list
        lines = [round(float(line),2) for line in lines]# sets each price value to a float rounded to two decimal places
    return lines


tsla_prices = import_stock("/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/hw4/TSLA.txt")

print(tsla_prices)