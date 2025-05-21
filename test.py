'''
3.14 @ 119th iteration
3.141 @ 1688th iteration
3.141 twice @ 2454-2455th iterations
'''
#inilization
numerator = 4
divisor = 1
pi_iteration = numerator/divisor #not including previous iterations
pi = pi_iteration #running full decimal calc of pi
addition_iteration = False #flips from addition to subtraction each iteration
iteration_counter = 1

def pi_N_digits(pi_var,N=4):
    return eval(str(pi_var)[:N]) #truncates pi leaving N number of digits...used to break loop...avoids scrolling endlessly through console
def Pi_print_iteration():
    return print(str(iteration_counter)+":  +"+str(numerator)+"/"+str(divisor), "=", end=" ")#prints each iteration for visual clarity

for i in range(3000):
    previous_pi = pi#used to find double accurances of 3.141
    Pi_print_iteration()
    print(pi)
    divisor += 2 #jumps to the next odd denominator for the next pi iteration
    pi_iteration = numerator/divisor
    if addition_iteration == True: #condition to switch to + or -
        pi = pi + pi_iteration
    else:
        pi = pi - pi_iteration
    addition_iteration = not addition_iteration #flips each iteration to use - or +
    iteration_counter += 1
    
    if pi_N_digits(pi,5) == pi_N_digits(previous_pi,5): #used to test if double accurance of 3.141 is found
        Pi_print_iteration()
        print(pi)
        break #found double accurance of 3.141...avoids scrolling endlessly through console