'''activity 1'''
name = input("What is your name: ")
color = input("What is your favorite color? ")
with open("PA_week5_activity1.txt", "w") as name_and_color:
    name_and_color.write(name,"\n", color)