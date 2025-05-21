#inilization
numerator = 4
divisor = 1
pi_iteration = numerator/divisor #not including previous iterations
pi = pi_iteration #running full decimal calc of pi
addition_iteration = False #flag to flip from addition to subtraction each iteration
iteration_counter = 1

def pi_N_digits(pi_var,N=4):
    return eval(str(pi_var)[:N]) #truncates pi leaving N number of digits...used to break loop
def Pi_print_iteration():
    return print(str(iteration_counter)+":  +"+str(numerator)+"/"+str(divisor), "=", end=" ")

for i in range(10000):
    previous_pi = pi
    Pi_print_iteration()
    print(pi)
    divisor += 2
    pi_iteration = numerator/divisor
    if addition_iteration == True:
        pi = pi + pi_iteration
    else:
        pi = pi - pi_iteration
    addition_iteration = not addition_iteration
    iteration_counter += 1
    
    if pi_N_digits(pi,6) == pi_N_digits(previous_pi,6):
        Pi_print_iteration()
        print(pi)
        break