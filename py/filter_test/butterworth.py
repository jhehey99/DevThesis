import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


Fs2 = 50
Wp = 10/Fs2
Ws = 60/Fs2
N, Wn = signal.buttord(Wp, Ws, 3, 60)
b, a = signal.butter(N, Wn, 'low', True)
w, h = signal.freqs(b, a, np.logspace(1, 2, 500))
plt.semilogx(w, 2 * np.log10(abs(h)))
plt.title('Butterworth bandpass filter fit to constraints')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.grid(which='both', axis='both')

print(N, Wn)
plt.show()