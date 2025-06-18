with open('/home/crostini/Github/Jacob_Cardon_data_3500_HW/HW/final_project/AAPL.csv') as csv_file:
    lines = csv_file.readlines()
    last_date = lines[-1].split(',')[0]
    oldest_date = lines[1].split(',')[0]
    print(oldest_date>last_date)