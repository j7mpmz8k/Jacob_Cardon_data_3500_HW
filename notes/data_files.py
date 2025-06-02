file_variable = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt", "r") # r=read(default) w=write a=append
content_variable = file_variable.read()#reads entire content of file
print(content_variable)
file_variable.close()#closes file

file_variable = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt")
lines_variable = file_variable.readlines()#
for line in lines_variable:
    print(line)
file_variable.close()


new_file = open("example.txt", "w")#creates new file in same file path as folder of this script
new_file.write("Hello world!\n")#write function does not add new line by default
new_file.close()
