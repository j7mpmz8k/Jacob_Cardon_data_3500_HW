#to convert from integer ie. 3 to floating number number ie. 3.0
float(3) 
#Out: 3.0


9//2 #floor division while truncating remainder
3**5 #3 to the power of 5
9%2 #modulus division leaving only remainder

#checks if number is even
import random
num = random.randint(0,10)
if num%2 == 0:
    print(num, "is even!")
else:
    print(num, "is odd")

#convert string to floating number as numbers input from user are strings
number = ("3.0") #string
number = eval(number)
print(number)
#Out: 3.0 #float or use float()

number = ("3") #string
number = eval(number)
print(number)
#Out: 3 #int OR use int()

#numbers input from user are strings, use eval() to convert
inputvariable = input("enter a number: ")
inputvariable = eval(inputvariable)

#augmented operators
age = 0 #initializing variable
age += 1
#this is the same as age = age + 1
#more:
age -= 1
age //= 1
age *= 1



#generates random number, imports 'random' library module
import random
print(random.randrange(1,4))# output: 1-3
print(random.randint(1,4))# output: 1-4
import numpy
print(numpy.random.randint(1, 4, size=10))#output: 1-3 with array of 10 random numbers

#math module(complete list at https://docs.python.org/3/library/math.html)
import math# returns floats
math.ceil(9.2)# rounds up
math.floor(9.2)# rounds down
math.fabs(-5)# absolute value
math.sqrt(16)# squareroot
math.fmod(7,4)# remainder, ie. 7/4=1 3/4...output: 3.0


import time
start_time = time.time()
print("hello world")
end_time = time.time()
time_lapsed_seconds = end_time - start_time
print("seconds to run script:", time_lapsed_seconds)