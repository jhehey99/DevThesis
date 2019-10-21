import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import sklearn.preprocessing as skpre
import pywt


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


np.random.seed(4)
ecg, noisy_ecg = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.4)

N = len(noisy_ecg)
print(N)

# plt.figure(0)
# plt.subplot(411)
# plt.plot(ecg)
#
#
# plt.subplot(412)
# plt.plot(noisy_ecg)


# apply single wavelet decomposition
# (cA, cD) = pywt.dwt(noisy_ecg, 'db8')
# # print(cA, cD)
#
# print(len(noisy_ecg))
# print(len(cA), len(cD))
#
# plt.subplot(413)
# plt.plot(cA)
#
# plt.subplot(414)
# plt.plot(cD)

# multi level wavelet decomposition

# cA2, cD2, cD1 = pywt.wavedec(noisy_ecg, 'db8', level=2)
#
# plt.figure(1)
#
#
# plt.subplot(411)
# plt.plot(noisy_ecg)
#
# plt.subplot(412)
# plt.plot(cA2)
#
# plt.subplot(413)
# plt.plot(cD2)
#
# plt.subplot(414)
# plt.plot(cD1)
lp_sos = signal.butter(5, 10, 'lowpass', fs=100, output='sos')

coeffs = pywt.wavedec(noisy_ecg, 'db4', level=4)
clen = len(coeffs)

to_plots = [noisy_ecg] + [signal.resample(s, N) for s in coeffs[1:]]
print(len(to_plots), clen)

plot_n = clen * 100 + 11
print(plot_n)

plt.figure(0)
for i, to_plot in enumerate(to_plots):
    plt.subplot(plot_n)
    plot_n += 1
    plt.plot(to_plot**2)
    plt.plot(ecg)

plt.tight_layout()
plt.show()

#
#
#
# def lowpassfilter(signal, thresh = 0.1, wavelet="db8", mode="zpd", level=6):
#     thresh = thresh*np.nanmax(signal)
#     coeff = pywt.wavedec(signal, wavelet, mode=mode, level=level)
#     coeff[1:] = (pywt.threshold(i, value=thresh, mode="soft") for i in coeff[1:])
#     reconstructed_signal = pywt.waverec(coeff, wavelet, mode=mode)
#     return reconstructed_signal
#
#
# threshold = 0.1
# step = 0.1
# max_fig_count = 5
#
# for fig_count in range(max_fig_count):
#
#     plt.figure(fig_count)
#
#     plt.subplot(411)
#     plt.plot(noisy_ecg)
#     plt.plot(ecg, 'r')
#
#     subplot_count = 412
#     for i in range(3):
#         filtered = lowpassfilter(noisy_ecg)
#         # filtered = lowpassfilter(noisy_ecg, threshold)
#
#         plt.subplot(subplot_count)
#         plt.plot(filtered)
#         plt.plot(ecg, 'r')
#         plt.title("Threshold = " + str(threshold))
#         threshold += step
#         subplot_count += 1
#
#     plt.tight_layout()
#     plt.show()


#
# # Thresholding
#
# cD_hat = cD / (cD**2).sum()**0.5
#
# variance = np.median(cD_hat) / 0.6745
# threshold = variance * np.sqrt(2*np.log(N))
# print(variance)
# print(threshold)
#
# thresdolded = pywt.threshold(noisy_ecg, threshold, 'hard')
# print(len(thresdolded))
# plt.figure(1)
# plt.subplot(211)
# plt.plot(thresdolded)
#
#
# # Inverse Wavelet Transform
#
# A = pywt.idwt(cA, cD, 'db2', 'sp1')
# plt.subplot(212)
# plt.plot(A)









