import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack

#TODO:
# ung 1st diastolic peak, earlier than 1st systolic peak
# and ung last systolic peak, later than last diastolic peak

print("========================")
# get arguments passed from node js
if len(sys.argv) > 1:
    data_path = sys.argv[1]
    fn_figure = sys.argv[2]
    show_plot = False

    print("Ran from Node.js")
    print("Processing", data_path)
    print("Figure Filename:", fn_figure)
else:
    # no arguments, ran from pycharm pag dito
    data_path = "ppg_test_data10"
    fn_figure = "ppg_leg_"
    show_plot = True
    print("Ran from Pycharm")
    print("Processing", data_path)

save_dir = "../../servers/server-websocket/public/result/"
f = open(data_path)

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

print("========================")
# get last time and first time to determine duration (s)
Ts = abs(time[-1] - time[0]) / 1000.0
N = len(time)
print("Duration: {}s | Number of Samples: {}".format(Ts, N))

# sampling frequency (N/Ts)
Fs = int(round(N/Ts))
print("Sampling Frequency: {}".format(Fs))

# 1st figure
fig1 = plt.figure(1, figsize=(10,6))

# original signal
plt.subplot(221)
plt.title("Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))


# fft of the original signal
T = 1.0 / 800.0
fft_freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)
fft_value = fftpack.fft(value)
plot_fft_value = 2.0/N * np.abs(fft_value[0:N//2])
plt.subplot(222)
plt.title("FFT of Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Frequency (Hz)")
plt.plot(fft_freqs, plot_fft_value)


# apply butterworth low pass filter
sos = signal.butter(5, 10, 'lowpass', fs=Fs, output='sos')
# filtered_value = np.round(signal.sosfilt(sos, value), 4)      # conventional
filtered_value = np.round(signal.sosfiltfilt(sos, value), 4)    # zero-phase
plt.subplot(223)
plt.title("5th Order 10 Hz Low Pass\nZero-Phase Butterworth Filter")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))


# fft of the filtered signal
# ewan ko bat ganun parin. pero mas maganda naman ung signal eh kaya okay na un
# filtered_fft_value = fftpack.fft(filtered_value)
# filtered_plot_fft_value = 2.0/N * np.abs(filtered_fft_value[0:N//2])
# plt.subplot(224)
# plt.plot(fft_freqs, filtered_plot_fft_value)

# try peak finding
peak_d = 20 # min no. of points between each peak
peak_h = round(max(filtered_value)/2)
print("Systolic Peak Finding: Height = {}, Distance = {}".format(peak_h, peak_d))
peaks, _ = signal.find_peaks(filtered_value, height=peak_h, distance=peak_d)
peak_times = [time[p] for p in peaks]
peak_values = [filtered_value[p] for p in peaks]
plt.subplot(224)
plt.title("Systolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(peak_times, peak_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# vertical line markers for systolic peaks
for sp in peaks:
    plt.axvline(time[sp], linestyle='--', color='gray')

# Systolic Peaks Properties
zip_sp = list(zip(peak_times, peak_values))
dist_sp = np.diff(peaks)
width_sp = np.diff(peak_times)
print("========================")
print("Systolic Peak Properties")
print(" >> Length:", len(zip_sp))
print(" >> Time and Values:", zip_sp)
print(" >> Distance:", dist_sp)
print(" >> Min Distance: {}, Max Distance: {}".format(min(dist_sp), max(dist_sp)))
print(" >> Average Distance:", round(np.average(dist_sp), 4))
print(" >> Width (ms):", width_sp)
print(" >> Min Width (ms): {}, Max Width (ms): {}".format(min(width_sp), max(width_sp)))
print(" >> Average Width (ms):", round(np.average(width_sp), 4))

# end figure 1
plt.tight_layout()
print("========================")
print("Figure 1 Saved...")
plt.savefig(save_dir + fn_figure + "fig1.svg", format="svg", bbox_inches='tight')


# 2nd figure
fig2 = plt.figure(2, figsize=(10,6))

# 1st derivative
grad = np.gradient(filtered_value)
# plt.plot(time, filtered_value)
# plt.plot(time, grad, color="red")

# 2nd derivative
grad2 = np.gradient(grad)
plt.subplot(221)
plt.title('Filtered with 2nd Derivative')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad2, color="red")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# lahat ng below 0 to above 0 transitions kunin natin
inflct_points = []
inflct_times = []
inflct_values = []

# may 1% allowance from 0 kaya -0.01
# kasi minsan may umangat pero nabitin sa 0 so lagyan allowance onti
ifp_allowance = -0.01
for i in range(grad2.__len__() - 1):
    p_cur = grad2[i]
    p_nxt = grad2[i+1]

    # eto ung pagkuha ng inflection points
    if p_cur < 0 and p_nxt >= ifp_allowance:
        inflct_points.append(i+1)
        inflct_times.append(time[i+1])
        inflct_values.append(grad2[i+1])

plt.subplot(222)
plt.title('Marked Inflection Points')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad2, color="red")
# plt.plot(inflct_times, inflct_values, 'x')
plt.plot(time, np.zeros_like(grad2), "--", color="gray")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

for inf_time in inflct_times:
    plt.axvline(inf_time, linestyle='--', color='gray')

# remove first inflection points after each peak
# print("INFLECTION")
# print("inflct point: ", inflct_points)
# print("peak times:", peak_times)
# print("inflct_times: ", inflct_times)

new_inflct_points = inflct_points.copy()
for pt in peak_times:
    for ifp in new_inflct_points:
        if time[ifp] >= pt:
            new_inflct_points.remove(ifp)
            break

new_inflct_times, new_inflct_values = [], []
for ifp in new_inflct_points:
    new_inflct_times.append(time[ifp])
    new_inflct_values.append(filtered_value[ifp])

# print("new_inflct_points: ", len(new_inflct_points), new_inflct_points)
# print("new_inflct_times: ", len(new_inflct_times), new_inflct_times)
# print("new_inflct_values: ", len(new_inflct_values), new_inflct_values)

plt.subplot(223)
plt.title('Removed Inflection After Peak')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad2, color="red")
plt.plot(time, np.zeros_like(grad2), "--", color="gray")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

for ift in new_inflct_times:
    plt.axvline(ift, linestyle='--', color='gray')


# final inflection point extraction
# remove inflection points below 20% the average (parang noise sya)
ave_ifv_val = np.average(new_inflct_values)
ave_ifv_low = ave_ifv_val * 0.3
ave_ifv_high = ave_ifv_val * 1.20
new2_inflct_points = [new_inflct_points[i] for i in range(len(new_inflct_values)) if new_inflct_values[i] >= ave_ifv_low and new_inflct_values[i] <= ave_ifv_high]
# new2_inflct_points = [ifp for ifp in new_inflct_points if filtered_value[ifp] >= ave_ifv_low]
# print("ave_ifv_low: ", ave_ifv_low)
# print("high", ave_ifv_high)
# print(new2_inflct_points)
# print("last", filtered_value[new2_inflct_points[-1]])
# print("new2_inflct_points: ", new2_inflct_points)

# plt.axhline(ave_ifv_low, linestyle='--', color='gray')
# plt.axhline(ave_ifv_high, linestyle='--', color='gray')

# difference in sample point between each marked inflection point
diff_ifp = np.diff(new2_inflct_points)
# print("diff_ifp: ", diff_ifp)

# min no. of pts between each inflection point, same as peak_d (20)
ifp_d = peak_d
diastolic_points = []

skip = False
j = 0
l_count = len(new2_inflct_points) - 1
for i in range(l_count):
    if skip: i = j; skip = False; continue
    j = i
    diastolic_points.append(new2_inflct_points[j])
    # pag last 2 points nung diastolic points sobrang magkalapit, tanggalin ung latest
    if len(diastolic_points) > 1 and abs(diastolic_points[-2] - diastolic_points[-1]) < ifp_d:
        diastolic_points.pop()

    while j < l_count and abs(new2_inflct_points[j + 1] - new2_inflct_points[j]) < ifp_d:
        skip = True
        j += 1


# para masama ung last peak. kung hindi sya iniskip due to margin
if not skip:
    diastolic_points.append(new2_inflct_points[-1])
    if len(diastolic_points) > 1 and abs(diastolic_points[-2] - diastolic_points[-1]) < ifp_d:
        diastolic_points.pop()

# print("diastolic_points: ", diastolic_points)

diastolic_times, diastolic_values = [], []
for dp in diastolic_points:
    diastolic_times.append(time[dp])
    diastolic_values.append(filtered_value[dp])

plt.subplot(224)
plt.title('Diastolic Peaks')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(diastolic_times, diastolic_values, 'x', color='r')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.axhline(ave_ifv_low, linestyle='--', color='gray')
# plt.axhline(ave_ifv_high, linestyle='--', color='gray')

# vertical line markers for diastolic peaks
for dp in diastolic_points:
    plt.axvline(time[dp], linestyle='--', color='gray')


# Diastolic Peak Properties
zip_dp = list(zip(diastolic_times, diastolic_values))
dist_dp = np.diff(diastolic_points)
width_dp = np.diff(diastolic_times)
print("========================")
print("Diastolic Peak Properties")
print(" >> Length:", len(zip_dp))
print(" >> Time and Values:", zip_dp)
print(" >> Distance (N):", dist_dp)
print(" >> Min Distance: {}, Max Distance: {}".format(min(dist_sp), max(dist_sp)))
print(" >> Average Distance:", round(np.average(dist_sp), 4))
print(" >> Width (ms):", width_dp)
print(" >> Min Width (ms): {}, Max Width (ms): {}".format(min(width_dp), max(width_dp)))
print(" >> Average Width (ms):", round(np.average(width_dp), 4))


# TODO: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# end figure 2
plt.tight_layout()
print("========================")
print("Figure 2 Saved...")
plt.savefig(save_dir + fn_figure + "fig2.svg", format="svg", bbox_inches='tight')


if show_plot:
    plt.show()



