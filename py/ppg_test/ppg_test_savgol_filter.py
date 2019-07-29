import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

f = open('ppg_test_data1')

data = []
time = []
value = []
for line in f:
    entry = line.strip().split(',')
    x, y = entry
    time.append(int(x))
    value.append(int(y))

print(time)
print(value)

plt.subplot(211)
plt.plot(time, value)


# apply savgol filter
filtered_value = savgol_filter(value, 11, 3)
plt.subplot(212)
plt.plot(time, filtered_value)

plt.show()

