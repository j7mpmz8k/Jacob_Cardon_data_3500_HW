#this only works for lists sinc they are mutable unlike tuples
def changeint(lst):
    lst[0] = 9999999
    return #in this case return doesn't matter

lst2 = [1,2,3,4,5]
changeint(lst2)
print(lst2)
#output: [9999999, 2, 3, 4, 5]