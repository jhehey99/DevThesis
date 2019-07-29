
# generate random PTT
# generate random Blood pressure
# generate regression model




# test regression w/ gradient descent example
import numpy as np
import matplotlib.pyplot as plt
import random
from random import uniform

plt.rcParams['figure.figsize'] = (12.0, 9.0)

# initialize seed
random.seed(1)

# generate random PTT and BP dataset
N = 100
PTT = [round(uniform(0, 2), 4) for i in range(N)]
SBP = [round(uniform(100, 200), 4) for i in range(N)]

print(PTT)
print(SBP)
plt.scatter(PTT, SBP)
plt.show()

