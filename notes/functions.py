#custom function definition for (a^b)+1
def raised_to_power_of_num_plus1(place_holder1=0, place_holder2=0):# "=0" is the default value if nothing entered
    combined_placeholder = place_holder1 ** place_holder2 #optional
    return combined_placeholder + 1 # "+1" could have also been in optional variable
print(raised_to_power_of_num_plus1(3, 2)) #(3^2)+1.....3 & 2 override 0 as default value