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
    data_path = "ppg_test_data12"
    # data_path = "ppg_test_data_leg1"
    fn_figure = "ppg_leg_"
    show_plot = True
    print("Ran from Pycharm")
    print("Processing", data_path)

save_dir = "../../servers/server-websocket/public/result/"
f = open(data_path)

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
T = 1.0 / 800.0
fft_freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)
fft_value = fftpack.fft(value)
plot_fft_value = 2.0/N * np.abs(fft_value[0:N//2])



# 3 low pass butterworth filter
sos = signal.butter(5, 10, 'lowpass', fs=Fs, output='sos')
# filtered_value = np.round(signal.sosfilt(sos, value), 4)      # conventional
filtered_value = np.round(signal.sosfiltfilt(sos, value), 4)    # zero-phase



# fft of the filtered signal
# ewan ko bat ganun parin. pero mas maganda naman ung signal eh kaya okay na un
# filtered_fft_value = fftpack.fft(filtered_value)
# filtered_plot_fft_value = 2.0/N * np.abs(filtered_fft_value[0:N//2])
# plt.subplot(224)
# plt.plot(fft_freqs, filtered_plot_fft_value)

# 4 systolic peak finding
peak_d = 20 # min no. of points between each peak
peak_h = round(max(filtered_value)/2)
print("Systolic Peak Finding: Height = {}, Distance = {}".format(peak_h, peak_d))
peaks, _ = signal.find_peaks(filtered_value, height=peak_h, distance=peak_d)
peak_times = [time[p] for p in peaks]
peak_values = [filtered_value[p] for p in peaks]

# get systolic points
systolic_points = peaks.tolist().copy()
systolic_times, systolic_values = [], []
for sp in systolic_points:
    systolic_times.append(time[sp])
    systolic_values.append(filtered_value[sp])

# 2nd figure
# 1st derivative
grad = np.gradient(filtered_value)
# 5 2nd derivative
grad2 = np.gradient(grad)


# lahat ng below 0 to above 0 transitions kunin natin
inflct_points = []
inflct_times = []
inflct_values = []

# 6 inflection points
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


# remove first inflection points after each peak
# print("INFLECTION")
# print("inflct point: ", inflct_points)
# print("peak times:", peak_times)
# print("inflct_times: ", inflct_times)

# 7 removed inflection after systolic peaks
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


# 8 diastolic peaks
# final inflection point extraction
# remove inflection points below 20% the average (parang noise sya)
ave_ifv_val = np.average(new_inflct_values)
ave_ifv_low = ave_ifv_val * 0.3
ave_ifv_high = np.average(peak_values) * 0.8
new2_inflct_points = [new_inflct_points[i] for i in range(len(new_inflct_values)) if new_inflct_values[i] >= ave_ifv_low]
# new2_inflct_points = [new_inflct_points[i] for i in range(len(new_inflct_values)) if new_inflct_values[i] >= ave_ifv_low and new_inflct_values[i] <= ave_ifv_high]
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
# get diastolic points
diastolic_times, diastolic_values = [], []
for dp in diastolic_points:
    diastolic_times.append(time[dp])
    diastolic_values.append(filtered_value[dp])


# get minima to determine reference point
minima_points = signal.argrelextrema(filtered_value, np.less)[0]
minima_points = [minima_points[i] for i in range(len(minima_points)) if filtered_value[minima_points[i]] <= 1]
minima_times = []
minima_values = []
for mp in minima_points:
    minima_times.append(time[mp])
    minima_values.append(filtered_value[mp])

reference_point, reference_time, reference_value = -1, -1, -1
if len(minima_points) > 0:
    reference_point, reference_time, reference_value = minima_points[0], minima_times[0], minima_values[0]

    # get systolic points after the reference point
    systolic_points = [systolic_points[i] for i in range(len(systolic_times)) if systolic_times[i] > reference_time]
    systolic_times, systolic_values = [], []
    for dp in systolic_points:
        systolic_times.append(time[dp])
        systolic_values.append(filtered_value[dp])
    
    # get diastolic points after the reference point
    diastolic_points = [diastolic_points[i] for i in range(len(diastolic_times)) if diastolic_times[i] > reference_time]
    diastolic_times, diastolic_values = [], []
    for dp in diastolic_points:
        diastolic_times.append(time[dp])
        diastolic_values.append(filtered_value[dp])


# 9, 10 final systolic/diastolic peak matching
final_systolic_points = peaks.tolist().copy()
final_systolic_times, final_systolic_values = [], []
for sp in final_systolic_points:
    final_systolic_times.append(time[sp])
    final_systolic_values.append(filtered_value[sp])
    
final_diastolic_points = diastolic_points.copy()
final_diastolic_times, final_diastolic_values = [], []
for dp in final_diastolic_points:
    final_diastolic_times.append(time[dp])
    final_diastolic_values.append(filtered_value[dp])

# remove all systolic peaks if it is BEFORE the first diastolic peak (IN FRONT)
for i in range(len(final_systolic_times)):
    if final_systolic_times[i] < final_diastolic_times[i]:
        final_systolic_points.pop(i); final_systolic_times.pop(i); final_systolic_values.pop(i);
    else:
        break

# remove all diastolic peaks if it is AFTER the last systolic peak (AT THE BACK)
for i in range(len(final_diastolic_times)):
    if final_diastolic_times[-1] > final_systolic_times[-1]:
        final_diastolic_points.pop(); final_diastolic_times.pop(); final_diastolic_values.pop();
    else:
        break

# remove trailing systolic peaks after last systolic-diastolic match
if len(final_diastolic_times) > 0:
    last_dpt = final_diastolic_times[-1]
    last_match_spi = -1

    # non-last systolic dapat kaya stop in length - 1
    for i in range(len(final_systolic_times) - 1):
        # unang non-last systolic na match nung last diastolic
        if final_systolic_times[i] > last_dpt:
            last_match_spi = i
            break

    if last_match_spi != -1:
        while last_match_spi < len(final_systolic_points):
            print(last_match_spi, " | len:", len(final_systolic_points))
            final_systolic_points.pop(); final_systolic_times.pop(); final_systolic_values.pop();
            last_match_spi += 1


# remove leading diastolic peaks before first systolic-diastolic match
if len(final_systolic_times) > 0:
    first_spt = final_systolic_times[0]
    first_match_dpi = -1

    # non-first diastolic dapat kaya stop is index 0
    for i in range(len(final_diastolic_times) -1, 0, -1):
        # unang non-first diastolic na match nung first systolic
        if final_diastolic_times[i] < first_spt:
            first_match_dpi = i
            break

    if first_match_dpi != -1:
        while first_match_dpi > 0:
            final_diastolic_points.pop(0); final_diastolic_times.pop(0); final_diastolic_values.pop(0);
            first_match_dpi -= 1



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

# 2 fft of the original signal
plt.subplot(222)
plt.title("FFT of Original Signal")
plt.ylabel("ADC Value")
plt.xlabel("Frequency (Hz)")
plt.plot(fft_freqs, plot_fft_value)

# 3 low pass butterworth filter
plt.subplot(223)
plt.title("5th Order 10 Hz Low Pass\nZero-Phase Butterworth Filter")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 4 systolic peak finding
plt.subplot(224)
plt.title("Initial Systolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(peak_times, peak_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# vertical line markers for systolic peaks
for sp in peaks:
    plt.axvline(time[sp], linestyle='--', color='gray')

# end figure 1
plt.tight_layout()
print("========================")
print("Figure 1 Saved...")
plt.savefig(save_dir + fn_figure + "fig1.svg", format="svg", bbox_inches='tight')

# 2nd figure
fig2 = plt.figure(2, figsize=fig_size)

# 5 2nd derivative
plt.subplot(221)
plt.title('Filtered with 2nd Derivative')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad2, color="red")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# 6 inflection points
plt.subplot(222)
plt.title('Marked Inflection Points')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad2, color="red")
plt.plot(time, np.zeros_like(grad2), "--", color="gray")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

for inf_time in inflct_times:
    plt.axvline(inf_time, linestyle='--', color='gray')

# 7 removed inflection after systolic peaks
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

# 8 diastolic peaks
plt.subplot(224)
plt.title('Initial Diastolic Peaks')
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



# end figure 2
plt.tight_layout()
print("========================")
print("Figure 2 Saved...")
plt.savefig(save_dir + fn_figure + "fig2.svg", format="svg", bbox_inches='tight')

# figure 3
fig3 = plt.figure(3, figsize=fig_size)
plt.subplot(211)
plt.title("Final Systolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(final_systolic_times, final_systolic_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
# vertical line markers for systolic peaks
for spt in final_systolic_times:
    plt.axvline(spt, linestyle='--', color='gray')

# if reference_point != -1:
#     plt.axvline(reference_time, linestyle='--', color='r')

plt.subplot(212)
plt.title("Final Diastolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(final_diastolic_times, final_diastolic_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
# vertical line markers for systolic peaks
for dpt in final_diastolic_times:
    plt.axvline(dpt, linestyle='--', color='gray')

# if reference_point != -1:
#     plt.axvline(reference_time, linestyle='--', color='r')

# end figure 3
plt.tight_layout()
print("========================")
print("Figure 3 Saved...")
plt.savefig(save_dir + fn_figure + "fig3.svg", format="svg", bbox_inches='tight')



# Systolic Peaks Properties
zip_sp = list(zip(final_systolic_times, final_systolic_values))
dist_sp = np.diff(final_systolic_points)
width_sp = np.diff(final_systolic_times)
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


# Diastolic Peak Properties
zip_dp = list(zip(final_diastolic_times, final_diastolic_values))
dist_dp = np.diff(final_diastolic_points)
width_dp = np.diff(final_diastolic_times)
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

if show_plot:
    plt.show()







