import padasip as pa
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import sklearn.preprocessing as skpre
import padasip.filters as paf


def sample_ecg(bpm: int, length: int, fs: int, noise_factor: float = 0.01, adc_bits: int = 10):
    # The "Daubechies" wavelet is a rough approximation to a real,
    # single, heart beat ("pqrst") signal
    pqrst = signal.wavelets.daub(8)

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


pqrst = signal.wavelets.daub(8)

ecg, noisy_ecg = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.1)

plt.figure(0)
plt.subplot(411)
plt.plot(ecg)


plt.subplot(412)
plt.plot(noisy_ecg)

lms = paf.FilterLMS(n=100, mu=0.1, w="random")
y, e, w = lms.run(np.array([ecg]), np.array([noisy_ecg]))
#
#
#
# plt.subplot(413)
# plt.plot(y)


# # creation of data
N = 500
x = np.random.normal(0, 1, (N, 4)) # input matrix
v = np.random.normal(0, 0.1, N) # noise
d = 2*x[:,0] + 0.1*x[:,1] - 4*x[:,2] + 0.5*x[:,3] + v # target

print(len(x))
print(x)
print(len(v))
print(len(d))

#
# # identification
# f = pa.filters.FilterLMS(n=1, mu=0.1, w="random")
# y, e, w = f.run(d, x)
#
# # show results
# plt.figure(figsize=(15,9))
# plt.subplot(211);plt.title("Adaptation");plt.xlabel("samples - k")
# plt.plot(d,"b", label="d - target")
# plt.plot(y,"g", label="y - output");plt.legend()
# plt.subplot(212);plt.title("Filter error");plt.xlabel("samples - k")
# plt.plot(10*np.log10(e**2),"r", label="e - error [dB]");plt.legend()




plt.tight_layout()
plt.show()