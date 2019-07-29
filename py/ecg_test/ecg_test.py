import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack


f = open("ecg_test_data2")

fig_size = (10, 6)


# process the input data
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

# 2 fft of the original signal
T = 1.0 / 800
fft_freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)
fft_value = fftpack.fft(value)
plot_fft_value = 2.0/N * np.abs(fft_value[0:N//2])


# 3 low pass butterworth filter
# sos = signal.butter(20, 10, 'lowpass', fs=Fs, output='sos')
# # filtered_value = np.round(signal.sosfilt(sos, value), 4)      # conventional
# filtered_value = np.round(signal.sosfiltfilt(sos, value), 4)    # zero-phase
#
# # 4 fft of the filtered signal
# filtered_fft_value = fftpack.fft(filtered_value)
# filtered_plot_fft_value = 2.0/N * np.abs(fft_value[0:N//2])



# Output

# 1st figure
fig1 = plt.figure(1, figsize=fig_size)
plt.subplot(221)
plt.title("Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 2 fft of the original signal
plt.subplot(222)
plt.title("FFT of Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Frequency (Hz)")
plt.ylim(top=20, bottom=-5)
# plt.plot(fft_freqs, np.abs(fft_value[0:N//2]))
plt.plot(fft_freqs, 2.0/N * np.abs(fft_value[:N//2]))


# 3 low pass butterworth filter
plt.subplot(223)
# plt.title("5th Order 10 Hz Low Pass\nZero-Phase Butterworth Filter")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 4 fft of the filtered signal
plt.subplot(224)
plt.title("FFT of Filtered Signal")
plt.ylabel("ADC Value")
plt.xlabel("Frequency (Hz)")
plt.ylim(top=5, bottom=-5)
plt.plot(fft_freqs, 2.0/N * np.abs(filtered_fft_value[0:N//2]))




plt.tight_layout()
plt.show()