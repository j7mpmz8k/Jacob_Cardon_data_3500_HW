#to reveal type
print(type('string'))
#Out: <class ‘str’>

print("Hello", end="") #unless specified, end parameter is set to \n by default after every output
print("World")
# Output: HelloWorld


, #concatenates with a space

+ #concatenates without a space

"\n" #prints new line

"\t" #prints with indented tab

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