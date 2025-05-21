pi = 0
neumerator = 4
devisor = 1

def fraction_iteration():
    return print(str(neumerator)+"/"+str(devisor), "=", neumerator/devisor)

for i in range(1000):
    # print(str(neumerator)+"/"+str(devisor), "=", neumerator/devisor)
    fraction_iteration()
    devisor += 2
