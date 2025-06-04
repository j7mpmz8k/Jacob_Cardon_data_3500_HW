# Activity 4
# initialize list of stings
strings = ["   hello  ", "whitespace      ", "   :)  "]

# list comprehension to remove whitespace
new_list = [string.strip() for string in strings]
print(new_list)

print(strings)