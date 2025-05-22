# 2.3
grade = float(input("What is your grade? "))
if grade >= float(90):
    print("Your grade of", grade, "earns you an A in this course!")
else:
    print("Sorry, your grade of", grade, "does not earn you an A in the course.")



# 2.4
left = 27.5
right = 2
print(left, "+", right, "=", left + right)
print(left, "-", right, "=",left - right)
print(left, "*", right, "=",left * right)
print(left, "/", right, "=",left / right)
print(left, "//", right, "=",left // right)
print(left, "**", right, "=",left ** right)



# 2.5
pi = 3.14159
r = 2
diameter = 2*r
circumference = 2*pi*r
area = pi*(r**2)
print("diameter:", diameter)
print("circumference:", circumference)
print("area:", area)



# 2.6
integer = int(input("enter an integer: "))
if integer % 2 == 0:
  print("The number", integer, "is even.")
else:
  print("The number", integer, "is odd.")



# 2.7
numA = 1024
numB = 10
divA = 4
divB = 2
if numA % divA == 0:
  print(numA, "is a multiple of",divA)
else:
  print(numA, "is not a multiple of", divA)

if numB % divB == 0:
  print(numB, "is a multiple of", divB)
else:
  print(numB, "is not a multiple of", divB)



# 2.8
print("number\tsquare\tcube")
for number in range(6):
    square = number ** 2
    cube = number ** 3
    print(str(number) + "\t" + str(square) + "\t" + str(cube))