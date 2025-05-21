# 3.14 @ 119th iteration
# 3.141 @ 1688th iteration
# 3.141 twice @ 2454-2455

neumerator = 4
devisor = 1
pi_iteration = neumerator/devisor
pi = pi_iteration
addition_iteration = False
iteration_counter = 1
previous_pi = pi

def fraction_iteration():
    return neumerator/devisor
def pi_N_digits(A=pi,N=4):
    return eval(str(A)[:N])

for i in range(3000):
    previous_pi = pi
    print(str(iteration_counter)+":  +"+str(neumerator)+"/"+str(devisor), "=", str(pi)[:5])
    devisor += 2
    pi_iteration = fraction_iteration()
    if addition_iteration == True:
        pi = pi + pi_iteration
    else:
        pi = pi - pi_iteration
    addition_iteration = not addition_iteration
    iteration_counter += 1
    
    if pi_N_digits(pi,5) == pi_N_digits(previous_pi,5):
        print(str(iteration_counter)+":  +"+str(neumerator)+"/"+str(devisor), "=", pi_N_digits(pi,5))
        break