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
'''Out: 1
        2
        3'''

#sentinel values are used as a unique input value to end a "while" loop
sentinal = -1
selection = 0
while selection > -1:
	print("\nChoose your selection from the following")
	selection = int(input("1 or 2\nEnter your selection: "))
	if selection == 1 or 2:
		print("selection noted, please try again")


for row in range(3):
	for col in range(4):
		print(row*col, end=" ")
	print()