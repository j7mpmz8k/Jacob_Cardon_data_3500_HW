#To check if two value are equal to each other, use ==
print(5 == 8)
#Out: false

#to check for not equal
print(5 != 8)
#Out: true

#IF statement syntax(must end with : and reported results must start with indentation
if 5 > 10:
	print("true")
else: #optional
	print("false")

#nested if statements use elif
grade = 75
if grade >= 90:
	print("A")
elif grade >= 80:
	print("B")
elif grade >= 70:
	print("C")
elif grade >= 60:
	print("D")
else:
	print("F")

#using while to repeat until false
age = 1
while age < 3:
	print("age: ", age)
	age = age + 1
else:
	print("Your age is now 3!")
#after false moves to this line
'''Out: 1
        2
        3'''

#for loop through a string
name = ("John")
for i in name:
	print("letter: ", i)