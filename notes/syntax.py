#to reveal type
print(type('string'))
#Out: <class ‘str’>

print("Hello", end="") #unless specified, end parameter is set to \n by default after every output
print("World")
# Output: HelloWorld


'string' = "string"
#use \" inside double quotes for nested strings
print("string \"string\" string")
#Or use single quotes inside double quotes
print("string 'string' string")
#Or vice versa
print('string "string" string') 

#Triple double quotes quotes for multi line string
print(""" 
this is the first line
This is the second line
This is the third line
""")

#Triple single quotes for multi line comments
'''
this is the first line
This is the second line
This is the third line
'''

#string contatenating
s1 = "happy"
s2 = "birthday"
s1 += " " + s2# has same function as s1 = s1+" "+s2
print(s1)# output: happy birthday

#repeating strings
repeating_string = "hi "
repeating_string *= 5
print(repeating_string)#output: hi hi hi hi hi 




#old list method
lst=[]
for i in range(1,4):
      i = float(i)# makes each item a float
      lst.append(i)# creates list of [1,2,3]
print(lst)#output: [1.0, 2.0, 3.0]

#new method, LIST COMREHENSION
new_lst = [float(i) for i in range(1,4)]# automatically appends i AND converts to a float
print(new_lst)#output: [1.0, 2.0, 3.0]



pi = "\t \n  3.14   \n\t"
print(pi.strip())#removes on both sides all whitepaces, tabs, new lines, ect.
print(pi.lstrip())#removes them from the left
print(pi.rstrip())#removes them from the right
