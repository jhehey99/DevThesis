import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import sklearn.preprocessing as skpre


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
    adc_resolution = (2**adc_bits) - 1

    # no noise
    ecg_sampled = signal.resample(ecg_template, num_samples)
    ecg_rescaled = skpre.minmax_scale(ecg_sampled, feature_range=(0, 1))
    final_ecg = adc_resolution * ecg_rescaled

    # noisy
    ecg_noisy_sampled = signal.resample(ecg_template_noisy, num_samples)
    ecg_noisy_rescaled = skpre.minmax_scale(ecg_noisy_sampled, feature_range=(0, 1))
    final_noisy_ecg = adc_resolution * ecg_noisy_rescaled

    return final_ecg, final_noisy_ecg


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


# Plot the sampled ecg signal
print("ecg simulation")
window = 20

ecg, noisy_ecg = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.5)
ave1 = moving_average(noisy_ecg, window)





lp_sos = signal.butter(50, 60, 'lowpass', fs=200, output='sos')
lp_val = np.round(signal.sosfiltfilt(lp_sos, noisy_ecg), 4)  # zero-phase
ave2 = moving_average(lp_val, window)



plt.figure(0)
plt.subplot(211)
plt.plot(noisy_ecg, 'b')
plt.plot(ave2, 'y')
# plt.plot(ecg, 'g')

plt.subplot(212)
plt.plot(noisy_ecg, 'r')
plt.plot(ave1, 'c')
plt.plot(ecg, 'g')
plt.tight_layout()


factor = 3
plt.figure(1)
ecg1, noisy_ecg1 = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.1*factor)
plt.subplot(411)
plt.plot(noisy_ecg1, 'b')
plt.plot(ecg, 'g')

ecg, noisy_ecg2 = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.2*factor)
plt.subplot(412)
plt.plot(noisy_ecg2, 'b')
plt.plot(ecg, 'g')

ecg, noisy_ecg3 = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.3*factor)
plt.subplot(413)
plt.plot(noisy_ecg3, 'b')
plt.plot(ecg, 'g')

ecg, noisy_ecg4 = sample_ecg(bpm=60, length=10, fs=100, noise_factor=0.4*factor)
plt.subplot(414)
plt.plot(noisy_ecg4, 'b')
plt.plot(ecg, 'g')






# plt.plot(ave2)
# plt.plot(lp_val)




plt.tight_layout()
plt.show()