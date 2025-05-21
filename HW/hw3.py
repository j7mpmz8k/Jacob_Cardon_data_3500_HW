'''
3.4
'''
for row in range(1,3):#sets up 2 rows
    for col in range(1,8):#sets up 7 columns
        print("@", end=" ")#prints 7 @'s without skipping to the next row
    print()#moves to the second row


'''
3.9
'''
num = int(input("Enter and integer between 7-10 digits: "))
divisor = 10**(len(str(num))-1)#divides by a power of 10 with equal length to length of num minus one "0"
temp_num = num
excluding_right = temp_num #finds all numbers exluding the first number on the left
first_num = temp_num // divisor #finds number on most left hand of input number

if len(str(num)) > 9 or len(str(num)) < 7:#makes sure input is 7-9 digits
    print("Error: integer must be 7-10 digits")
else:
    for i in range(len(str(num))): #itterations equal to as many digits in input number
        print(int(first_num))
        excluding_right %= divisor #divide by divisor to find all numbers exluding furthest number to the left
        first_num = excluding_right // (divisor/10) #divide divisor by 10 here to avoid division by zero error on last itteration
        divisor //= 10 #decreases divisor by one less digit


'''
3.11
'''
#initializing balances
gallons_total = 0
gallons_trip = 0
miles_total = 0
miles_trip = 0

log_status = 0#neutral flag for message loop

#avg calculations setup
def miles_per_gal():
    return miles_trip/gallons_trip
def total_avg():
    return miles_total/gallons_total

#message loop to update gas/miles tip log
while log_status != -1:#sentinal
    gallons_trip = int(input("Enter the gallons used (-1 to end): "))
    log_status = gallons_trip#checking if gallons entered is sentinal
    if log_status == -1:
        break
    else:
        gallons_total += gallons_trip#adding gal used in trip to total
        miles_trip = int(input("Enter the miles driven: "))
        miles_total += miles_trip#adding miles used in trip to tal
        print("\nThe miles/gallon for this tank was", miles_per_gal(), "\n")
print("\nThe overall average miles/gallon was", total_avg(),"\n")#exit message w/total avg