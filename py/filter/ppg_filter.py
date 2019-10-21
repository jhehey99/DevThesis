import sys
import numpy as np
import scipy.signal as signal


if len(sys.argv) > 1:
    script, count, values = sys.argv

    count = int(count)
    values = np.array([int(v) for v in values.split(',')])
    # print(count)
    # print(values)

    T = 5
    Fs = 100


    # low pass
    lp_sos = signal.butter(10, 5, 'lowpass', fs=Fs, output='sos')
    lp_val = np.round(signal.sosfiltfilt(lp_sos, values), 4)  # zero-phase
    filtered_value = lp_val

    print(list(filtered_value))
