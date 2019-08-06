import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack
import scipy.interpolate as ip

# setup
data_path = "../ppg_test/ppg_test_data12"
f = open(data_path)
fig_size = (6, 4)


# read the input data
data = []
time = []
value = []
for line in f:
    entry = line.strip().split(',')
    x, y = entry
    time.append(int(x))
    value.append(int(y))

time = np.array(time)
value = np.array(value)

# 1 original signal
print("========================")
# get last time and first time to determine duration (s)
Ts = abs(time[-1] - time[0]) / 1000.0
N = len(time)
print("Duration: {}s | Number of Samples: {}".format(Ts, N))

# sampling frequency (N/Ts)
Fs = int(round(N/Ts))
print("Sampling Frequency: {}".format(Fs))

# 2 interpolate linear
f = ip.interp1d(time, value)
t_new = np.linspace(time[0], time[-1], num=6000)

plt.subplot(222)
plt.plot(t_new, f(t_new))

# 3 interpolate cubic
fc = ip.interp1d(time, value, kind="cubic")
plt.subplot(223)
plt.plot(t_new, fc(t_new))


# Output

# 1st figure
fig1 = plt.figure(1, figsize=fig_size)

# 1 original signal
plt.subplot(221)
plt.title("Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))




plt.show()