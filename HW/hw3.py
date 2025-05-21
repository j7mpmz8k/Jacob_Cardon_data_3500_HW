'''
3.4
Fill in the Missing Code
'''
for row in range(1,3):#sets up 2 rows
    for col in range(1,8):#sets up 7 columns
        print("@", end=" ")#prints 7 @'s without skipping to the next row
    print()#moves to the second row


'''
3.9
Seperating the Digits in an Integer
'''
num = int(input("Enter and integer between 7-10 digits: "))
divisor = 10**(len(str(num))-1)#divides by a power of 10 with equal length to length of num minus one "0"
temp_num = num
excluding_left = temp_num #finds all numbers excluding the first number on the left
first_num = temp_num // divisor #finds number on most left hand of input number

if len(str(num)) > 10 or len(str(num)) < 7:#makes sure input is 7-10 digits
    print("Error: integer must be 7-10 digits")
else:
    for i in range(len(str(num))): #iterations equal to as many digits in input number
        print(int(first_num))
        excluding_left %= divisor #divide by divisor to find all numbers excluding furthest number to the left
        first_num = excluding_left // (divisor/10) #divide divisor by 10 here to avoid division by zero error on last iteration
        divisor //= 10 #decreases divisor by one less digit


'''
3.11
Miles per gallon
'''
#initializing balances
gallons_total = 0
gallons_trip = 0
miles_total = 0

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


'''
3.12
Palindrome
'''
num = int(input("\nPlease enter a 5 digit number: "))
if num < 10000 or num > 99999:#checks if input is 5 digits
    print("\nError: That is not a 5 digit number.\n")
else:
    #variable initializing
    last_num = num % 10
    rev_num = last_num
    excluding_last_num = num

    for i in range(len(str(num))-1):#reduces iteration by 1 since reversed number was already initialized with the last digit
        excluding_last_num = excluding_last_num // 10#shaves off last number each iteration
        last_num = excluding_last_num % 10#finds last number each iteration
        rev_num = rev_num * 10 + last_num#multiply by 10 so 0 can be a placeholder to add the next digit from the last number
    if num == rev_num:#checking if input number is the same as the reverse
        print("\nPalindrome!\n")
    else:
        print("\nNot a palindrome.\n")