num1 = 3
num2 = 7

listcomprehension = [[row*col for col in range(1,num2+1)] for row in range(1,num1+1)]
print(listcomprehension)
