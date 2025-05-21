#make a variable
pi_string = ("3.14")
pi_float = 3.14
not_pi_int = 314

#range creates a list of numbers between two numbers
r = range(3,-5,-2) #(start,stop,steps)
print(list(r))
#Out: 3,1,-1,-3,-5

for i in range(0,4):
	print(i)
#Out: 0,1,2,3,4

#for loop through a string
name = ("John")
for i in name:
	print("letter: ", i)

#for loop w/ list outputs each item in list
colors = ["red", "blue", "green"]
for i in colors:
	print("color: ", i)


#sum total of list & count of items in list
grades = [50, 45, 48, 10]
total = 0
num_grades = 0
for i in grades:
	total += i
	num_grades += 1
	print(total,num_grades)


# Slice notation to reverse the string
num_str = [3,4,5,2]
reversed_str = num_str[::-1] # Slice notation to reverse the string