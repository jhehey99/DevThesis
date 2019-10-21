import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import sklearn.preprocessing as skpre
import pywt


def sample_ecg(bpm: int, length: int, fs: int, noise_factor: float = 0.01, adc_bits: int = 10):
    # The "Daubechies" wavelet is a rough approximation to a real,
    # single, heart beat ("pqrst") signal
    pqrst = signal.wavelets.daub(4)

    # Add the gap after the pqrst when the heart is resting.
    samples_rest = 10
    zero_array = np.zeros(samples_rest, dtype=float)
    pqrst_full = np.concatenate([pqrst, zero_array])

    # Simulated Beats per minute rate
    # For a health, athletic, person, 60 is resting, 180 is intensive exercising
    bps = bpm / 60

    # Caculate the number of beats in capture time period
    # Round the number to simplify things
    num_heart_beats = int(length * bps)

    # Concatonate together the number of heart beats needed
    ecg_template = np.tile(pqrst_full, num_heart_beats)

    # Add random (gaussian distributed) noise
    noise = np.random.normal(0, noise_factor, len(ecg_template))
    ecg_template_noisy = noise + ecg_template

    # Simulate ECG coming from ADC
    num_samples = fs * length
    adc_resolution = (2 ** adc_bits) - 1

    # no noise
    ecg_sampled = signal.resample(ecg_template, num_samples)
    ecg_rescaled = skpre.minmax_scale(ecg_sampled, feature_range=(0, 1))
    final_ecg = adc_resolution * ecg_rescaled

    # noisy
    ecg_noisy_sampled = signal.resample(ecg_template_noisy, num_samples)
    ecg_noisy_rescaled = skpre.minmax_scale(ecg_noisy_sampled, feature_range=(0, 1))
    final_noisy_ecg = adc_resolution * ecg_noisy_rescaled

    return final_ecg, final_noisy_ecg


f = open("../ecg_test/ecg_test_data5")



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
value = np.array(value) * -1


np.random.seed(4)
ecg, noisy_ecg = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.4)


##
lp_sos = signal.butter(10, 5, 'lowpass', fs=100, output='sos')
lp_val = np.round(signal.sosfiltfilt(lp_sos, value), 4)  # zero-phase

# ecg = lp_val
# noisy_ecg = value
##

N = len(noisy_ecg)
print(N)

plt.figure(0)
plt.subplot(211)
plt.plot(ecg)

plt.subplot(212)
plt.plot(noisy_ecg)
plt.tight_layout()


# cwt
plt.figure(1)
wavelet = 'morl'
scales = np.arange(60, 100)
m = 'conv'

coef1, freqs1 = pywt.cwt(data=ecg, scales=scales, wavelet=wavelet,)
coef2, freqs2 = pywt.cwt(data=noisy_ecg, scales=scales, wavelet=wavelet)

print(pywt.scale2frequency(wavelet, scales) / 0.01)

# print(freqs1)
# print(freqs2)
print(len(coef2))
print(len(coef2[0]))
# print(coef2[0])

print(type(coef2))
print(type(coef2[0]))

plt.subplot(211)
plt.imshow(coef1)
plt.subplot(212)
plt.imshow(coef2)
plt.tight_layout()


ungx = np.arange(0, N)
ungy = scales
ungx, ungy = np.meshgrid(ungx, ungy)
ungz = coef2

# Clip negative values
# maxmax = np.max(coef2)
# ungz = np.clip(coef2, 0, maxmax)


# plot the 3d surface
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


fig = plt.figure(11)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(ungx, ungy, ungz, cmap=cm.viridis,
                       linewidth=0, antialiased=False)

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)


print(np.shape(coef2))


# try to convert it to 1d signal using average
new_coef2 = []
ave_cols = []
for j in range(len(coef2[0])):
    col = []
    for i in range(len(coef2)):
        element = coef2[i][j]
        col.append(element)

    new_coef2.append(col)
    ave_cols.append(np.average(col))

print(np.shape(new_coef2))
print(np.shape(ave_cols))
print(ave_cols)

plt.figure(5)
plt.plot(ave_cols)
# plt.plot(ecg)































# get the min and max
# z-axis = (val - min)/ (min-max) * height


#
# plt.figure(2)
# wavelet = 'gaus2'
#
# coef1, freqs1 = pywt.cwt(ecg, np.arange(1, 129), wavelet=wavelet)
# coef2, freqs2 = pywt.cwt(noisy_ecg, np.arange(1, 129), wavelet=wavelet)
#
# print(freqs1)
# print(freqs2)
#
#
# plt.subplot(211)
# plt.imshow(coef1)
# plt.subplot(212)
# plt.imshow(coef2*2)
# plt.tight_layout()
#
#
# plt.figure(3)
# wavelet = 'gaus3'
#
# coef1, freqs1 = pywt.cwt(ecg, np.arange(1, 129), wavelet=wavelet)
# coef2, freqs2 = pywt.cwt(noisy_ecg, np.arange(1, 129), wavelet=wavelet)
#
# print(freqs1)
# print(freqs2)
#
#
# plt.subplot(211)
# plt.imshow(coef1)
# plt.subplot(212)
# plt.imshow(coef2*2)
# plt.tight_layout()
#
#
# plt.figure(4)
# wavelet = 'gaus4'
#
# coef1, freqs1 = pywt.cwt(ecg, np.arange(1, 129), wavelet=wavelet)
# coef2, freqs2 = pywt.cwt(noisy_ecg, np.arange(1, 129), wavelet=wavelet)
#
# print(freqs1)
# print(freqs2)
#
#
# plt.subplot(211)
# plt.imshow(coef1)
# plt.subplot(212)
# plt.imshow(coef2*2)
# plt.tight_layout()
#


plt.show()



