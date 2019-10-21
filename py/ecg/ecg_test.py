import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack

f = open("ecg_sample_6")

fig_size = (10, 6)

# process the input data
count = 0
value = []
for line in f:
    entry = line.strip()
    value.append(int(entry))


value = np.array(value)

# 1 original signal
print("========================")
# get last time and first time to determine duration (s)
# Ts = abs(time[-1] - time[0]) / 1000.0
N = len(value)
# print("Duration: {}s | Number of Samples: {}".format(Ts, N))

# sampling frequency (N/Ts)
# Fs = int(round(N/Ts))
Fs = 100
# print("Sampling Frequency: {}".format(Fs))

# 2 fft of the original signal
T = 1.0 / 800
fft_freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)
fft_value = fftpack.fft(value)
plot_fft_value = 2.0/N * np.abs(fft_value[0:N//2])

# 3 10th order bandpass, 0.5 and 10 Hz cutoff frequencies
sos = signal.butter(10, [0.5, 10], 'bandpass', fs=Fs, output='sos')
filtered_value = np.round(signal.sosfiltfilt(sos, value), 4)   # zero-phase


# 4 R-peak finding

filtered_value_2 = filtered_value
vmax = np.max(filtered_value_2)
threshold = 0.50
vthresh = vmax* threshold
print(vthresh)

peaks, _ = signal.find_peaks(filtered_value_2, height=vthresh)

peaks_x = [list(range(N))[p] for p in peaks]
peaks_y = [filtered_value[p] for p in peaks]

# Output
# 1st figure
fig1 = plt.figure(1, figsize=fig_size)
plt.subplot(221)
plt.title("Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 2 fft of the original signal
plt.subplot(222)
plt.title("FFT of Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Frequency (Hz)")
plt.ylim(top=100, bottom=-5)
# plt.plot(fft_freqs, np.abs(fft_value[0:N//2]))
plt.plot(fft_freqs, 2.0/N * np.abs(fft_value[:N//2]))

# 3 low pass butterworth filter
plt.subplot(223)
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 4 ecg r peaks
plt.subplot(224)
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(filtered_value)
plt.plot(peaks_x, peaks_y, 'x', color='red')
plt.axhline(vthresh, color='red', linestyle='dashed')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))



plt.tight_layout()
plt.show()
