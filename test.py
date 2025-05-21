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