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

#append an element to the end of a list
lst = ["abc"]
lst.append("xyz")
print(lst)# output: ['abc', 'xyz']

#extend a list into another list
lst1 = [1,2,3]
lst2 = ["a","b","c"]
print(lst2)
lst1.extend(lst2)
print(lst1)# output: [1, 2, 3, 'a', 'b', 'c']

#inserts element to an indexed position
abc_list = ["a","b","c"]
abc_list.insert(1,"Hello!")
print(abc_list)# output: ['a', 'Hello!', 'b', 'c']


#slicing a list
list_w_index_position = [0,1,2,3,4,5,6,7,8,9,10]
list_w_index_position[2:5]#syntax: [cuts off index's prior this position(default=0), retreives index position ranges from 0 to this position minus prior syntax value (default=infinity)]
#output: [2, 3, 4]


#this only works for lists since they are mutable unlike tuples
def changeint(lst):
    lst[0] = 9999999#alters an index position of a list
    return #in this case return doesn't matter
lst2 = [1,2,3,4,5]
changeint(lst2)
print(lst2)
#output: [9999999, 2, 3, 4, 5]


#How to sort a list using .sort
lst = [3,6,4,2,5,2]
lst.sort()
print(lst)
#output: [2, 2, 3, 4, 5, 6]


#finds index position of an input using .index
colors = ["red", "blue", "green", "purple"]
print(colors.index("blue"))
#output: 1


#uses .rjust to right alight output
colors = ["red", "blue", "green", "purple"]
max_length = 0
for color in colors: #finds largest item in list
    if len(color) > max_length:
        max_length = len(color)
for color in colors:
    print(color.rjust(max_length))#uses max_length variable to avoid right alighting too more than needed and adjust according to changes in list
    for letter in color:
        print(letter.rjust(max_length))


#numpy arrays are faster than lists and take up less memory
import numpy #aslo may include "as np to store numpy as variable" ie. import numpy as np
list_example = [0,1,2,3,4,5]
np_array = numpy.array(list_example)#output: [0 1 2 3 4 5]....note that there are no comma seperators

array_of_zeros = numpy.zeros(100)#array of 100 zeros
array_of_ones = numpy.ones(100)#array of 100 ones