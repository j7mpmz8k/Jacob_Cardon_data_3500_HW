#to convert from integer ie. 3 to floating number number ie. 3.0
float(3) 
#Out: 3.0

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
inputvariable = eval(inputvariable)

#augmented operators
age += 1
#this is the same as age = age + 1
#more:
age -= 1
age //= 1
age *= 1