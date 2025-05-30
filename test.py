'''activity 5.2'''
file = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt")
file_lines = file.readlines()
complete_price_list = []

#converting list to a list of floats
for stock_price_local in file_lines:
    stock_price_local = float(stock_price_local)
    complete_price_list.append(stock_price_local)

#calculates average
def movingavg_Ndays_Nthstartingday(set_of_numbers, days=None, first=True):# syntax(list of numbers, numbers of days to average, counting from first or last)
    if days == None:
        days = int(len(set_of_numbers))#if no days are input represented by 'None', then every day becomes default
    if first == False:
        extracted_days = set_of_numbers[-days:]
        first_or_last = "Last"
    else:
        extracted_days = set_of_numbers[:days]
        first_or_last = "First"
    number_of_days_local = int(len(extracted_days))
    return sum(extracted_days)/number_of_days_local, number_of_days_local, first_or_last# reports average & number of days...this method is becuase defined functions can't update global variables

#calculates which index position to find last set of number from list of stock complete_price_list...used as the third syntax in 'movingavg_Ndays_Nthstartingday'
def last_numbers(numbers):
    return int(len(complete_price_list))-numbers+1


Nth_day_avg, Nth_number_of_days, first_or_last = movingavg_Ndays_Nthstartingday(complete_price_list, 4)# extracts avg & num of days into seperate variables from defined function
print(first_or_last,Nth_number_of_days,"days:", "$"+str(Nth_day_avg))

Nth_day_avg, Nth_number_of_days, first_or_last = movingavg_Ndays_Nthstartingday(complete_price_list, 4, False)# re-updates avg & num of days
print(first_or_last, Nth_number_of_days, "day average:", "$"+str(Nth_day_avg))

print()

# set up iterator values and trading variables
day_number = 0
buy = 0
total_profit = 0

# loop through complete_price_list
for price in complete_price_list:
    if day_number >= 4: # only begin 4 day average once there are 4 days to backtrack to
        avg = (complete_price_list[day_number] + complete_price_list[day_number - 1] + complete_price_list[day_number - 2] + complete_price_list[day_number - 3]) / 4
        if price < avg and buy == 0: # buy conditions
            buy = price
            print("Buying at:", "\t", price)
        elif price > avg and buy != 0: # sell conditions
            trade_profit = price - buy
            print("Selling at:", "\t", price)
            print("Trade profit:", "\t", trade_profit)
            total_profit += trade_profit
            buy = 0
            
    day_number += 1
   
print("total_profit:", "\t", total_profit)