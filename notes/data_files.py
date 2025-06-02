file_variable = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt", "r") # r=read(default) w=write a=append
content_variable = file_variable.read()#reads entire content of file
print(content_variable)
file_variable.close()#closes file or else python wont close till entire script is done running

file_variable = open("/home/crostini/Github/Jacob_Cardon_data_3500_HW/Programming_Activities/files/PA5data.txt")
lines_variable = file_variable.readlines()#
for line in lines_variable:
    print(line)
file_variable.close()


new_file = open("example.txt", "w")#creates new file in same file path as parent folder of this script...ie."Jacob_cardon_data_3500_HW"
new_file.write("Hello world!\n")#write function does not add new line by default
new_file.close()

#opening using with automatically closes file after loop is done
with open("example.txt1", "w") as with_as_file: #local variable
    with_as_file.write("hello again!\n")



import os # more functions for interacting with operating system
os.rename("old_file_name.txt", "renamed_file.txt")
os.mkdir("new_directory_name")# default file path under parent directory ie."Jacob_cardon_data_3500_HW"
os.system("mkdir -p new_directory/sub_directory")# passes linux command to operating system