'''
3.14 @ 119th iteration
3.141 @ 1688th iteration
3.141 twice @ 2454-2455th iterations
-Uses a for loop to iterate many times, each iteration calculating each new fraction with prior fractions. 
Uses an if statment to govern a bolean value to switch back and forth between addition and subtraction.
-To avoid scrolling endlessly through terminal to find repeating iterations of 3.141...I truncated PI leaving only the first 3 digits after the decimal.
I compare the truncated calculation with 3.141 and if not equal then the loop does not break until 3000 iterations have passes in the for loop
-I print the iteration count, the fraction, and the running pi calculation in terminal
'''
#inilization
numerator = 4
divisor = 1
pi_iteration = numerator/divisor #not including previous iterations
pi = pi_iteration #running full decimal calc of pi
addition_iteration = False #flips from addition to subtraction each iteration
iteration_counter = 1

#truncates pi leaving N number of digits...used to break loop...avoids scrolling endlessly through console
def pi_N_digits(pi_var,N=4):
    return eval(str(pi_var)[:N])

#prints out the iteration number, + or - the iteration fraction, along with the running total of PI
# - or + logic is inversed due to boolean flag not updated yet
def Pi_print_iteration():
    if addition_iteration == True:
        return print(str(iteration_counter)+":  -"+str(numerator)+"/"+str(divisor), "=", pi)
    else:
        return print(str(iteration_counter)+":  +"+str(numerator)+"/"+str(divisor), "=", pi)

#loop to calculate pi for each new iteration
for i in range(3000):
    previous_pi = pi#used to find double accurances of 3.141
    Pi_print_iteration()
    divisor += 2 #jumps to the next odd denominator for the next pi iteration
    pi_iteration = numerator/divisor

    #condition to switch to + or -
    if addition_iteration == True: 
        pi += pi_iteration
    else:
        pi -= pi_iteration

       
    addition_iteration = not addition_iteration #flips each iteration to use - or +
    iteration_counter += 1
    
    #statement to find where 3.141 occurs twice
    if pi_N_digits(pi,5) == pi_N_digits(previous_pi,5): #used to test if double accurance of 3.141 is found
        Pi_print_iteration()
        break