'''
3.4
Fill in the Missing Code
prints 7col and 2row of @
'''
for row in range(1,3):#sets up 2 rows
    for col in range(1,8):#sets up 7 columns
        print("@", end=" ")#prints 7 @'s without skipping to the next row
    print()#moves to the second row


'''
3.9
Seperating the Digits in an Integer
Uses floor and modulo division against a divisor to truncate the first number.
The divisor is as many digits as the input has which updates to be one less after each iteration as the input number is truncated each iteration in the for loop.
'''
num = int(input("Enter and integer between 7-10 digits: "))
divisor = 10**(len(str(num))-1)#divides by a power of 10 with equal length to length of num minus one "0"
temp_num = num
excluding_left = temp_num #finds all numbers excluding the first number on the left
first_num = temp_num // divisor #finds number on most left hand of input number

#makes sure input is 7-10 digits
if len(str(num)) > 10 or len(str(num)) < 7:
    print("Error: integer must be 7-10 digits")
    
else:#iterations equal to as many digits in input number
    for i in range(len(str(num))): 
        print(int(first_num))
        excluding_left %= divisor #divide by divisor to find all numbers excluding furthest number to the left
        first_num = excluding_left // (divisor/10) #divide divisor by 10 here to avoid division by zero error on last iteration
        divisor //= 10 #decreases divisor by one less digit


'''
3.11
Miles per gallon
relies on updating balance each while loop iteration. Uses a break to end loop when sentinal is typed
'''
#initializing balances
gallons_total = 0
gallons_trip = 0
miles_total = 0

#neutral flag for message loop
log_status = 0

#avg calculations setup
def miles_per_gal():
    return miles_trip/gallons_trip
def total_avg():
    if gallons_total == 0:
        return #prevents division by zero due to gallons_total being zero at first iteraton
    return miles_total/gallons_total

#message loop to update gas/miles trip log
while log_status != -1:#sentinal
    gallons_trip = int(input("Enter the gallons used (-1 to end): "))
    log_status = gallons_trip#checking if gallons entered is sentinal
    if log_status == -1:
        break#backs out of the trip log
    #continues trip log since sentinal was not entered
    else:
        gallons_total += gallons_trip#adding gal used in trip to total
        miles_trip = int(input("Enter the miles driven: "))
        miles_total += miles_trip#adding miles used in trip to tal
        print("\nThe miles/gallon for this tank was", miles_per_gal(), "\n")
print("\nThe overall average miles/gallon was", total_avg(),"\n")#exit message w/total avg


'''
3.12
Palindrome
-Uses a for loop which trancates the last number each iteration and then updating the left over number for the next iteration
-I store a variable adding the last number to the end of it which flips the input integer backwards
-If the backwards integer and the original are the same then it is a palindrome!
'''
#asks user and checks if input number is in fact 5 digets
num = int(input("\nPlease enter a 5 digit number: "))
if num < 10000 or num > 99999:#checks if input is 5 digits
    print("\nError: That is not a 5 digit number.\n")
else:
    #variable initializing
    last_num = num % 10
    rev_num = last_num
    excluding_last_num = num
    
    #for loop to find the reverse input integer
    for i in range(len(str(num))-1):#reduces iteration by 1 since reversed number was already initialized with the last digit
        excluding_last_num = excluding_last_num // 10#shaves off last number each iteration
        last_num = excluding_last_num % 10#finds last number each iteration
        rev_num = rev_num * 10 + last_num#multiply by 10 so 0 can be a placeholder to add the next digit from the last number
    if num == rev_num:#checking if input number is the same as the reverse
        print("\nPalindrome!\n")
    else:
        print("\nNot a palindrome.\n")


'''
3.14 @ 119th iteration
3.141 @ 1688th iteration
3.141 twice @ 2454-2455th iterations
-Uses a for loop to iterate many times, each iteration calculating each new fraction with prior fractions. 
Uses an if statment to govern a bolean value to switch back and forth between addition and subtraction.
-To avoid scrolling endlessly through terminal to find repeating iterations of 3.141...I truncated PI leaving only the first 3 digits after the decimal.
I compare the truncated calculation with 3.141 and if not equal then the loop does not break until 3000 iterations have passes in the for loop
-I print the iteration count, the fraction, and the running pi calculation in terminal
'''
#inilization
numerator = 4
divisor = 1
pi_iteration = numerator/divisor #not including previous iterations
pi = pi_iteration #running full decimal calc of pi
addition_iteration_status = False #flips from addition to subtraction each iteration
iteration_counter = 1

#truncates pi leaving N number of digits...used to break loop...avoids scrolling endlessly through console
def pi_N_digits(pi_var,N=4):
    new_pi = 0
    pi_var *= (10**(N-1))
    for i in str(pi_var):
        if i == ".":
            break
        else:
            new_pi = new_pi*10 + int(i)
    return new_pi

#prints out the iteration number, + or - the iteration fraction, along with the running total of PI
# - or + logic is inversed due to boolean flag not updated yet
def Pi_print_iteration():
    if addition_iteration_status == True:
        return print(str(iteration_counter)+":  -"+str(numerator)+"/"+str(divisor), "=", pi)
    else:
        return print(str(iteration_counter)+":  +"+str(numerator)+"/"+str(divisor), "=", pi)

#loop to calculate pi for each new iteration
for i in range(3000):
    previous_pi = pi#used to find double accurances of 3.141
    Pi_print_iteration()
    divisor += 2 #jumps to the next odd denominator for the next pi iteration
    pi_iteration = numerator/divisor

    #condition to switch to + or - upating the running total of pi
    if addition_iteration_status == True: 
        pi += pi_iteration
    else:
        pi -= pi_iteration

       
    addition_iteration_status = not addition_iteration_status #flips each iteration to use - or +
    iteration_counter += 1
    
    #statement to find where 3.141 occurs twice
    if pi_N_digits(pi,4) == pi_N_digits(previous_pi,4): #used to test if double accurance of 3.141 is found
        Pi_print_iteration()
        break