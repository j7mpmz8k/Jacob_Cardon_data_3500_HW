import numpy
import random

randoms = []
for i in range(10):
    randoms.append(random.randint(1,50))
print(randoms)

rands = numpy.random.randint(50, size=10)
print(rands)