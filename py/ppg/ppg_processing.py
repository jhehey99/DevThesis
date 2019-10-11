import sys
from typing import Optional, Union, Tuple, Any
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from numpy.core._multiarray_umath import ndarray
from scipy.interpolate import interp1d


filtered_value: Union[ndarray, Any]
Fs: int
interp_fft_freqs: Union[ndarray, Tuple[ndarray, Optional[float]]]
interp_fft_values: float
input_time: ndarray
input_value: ndarray
time: ndarray
interp_value: ndarray
interp_N: int

fig_num = 1
# file_nums = [ 8 ]
file_nums = range(1, 12)
save_dir = "../../servers/server-websocket/public/result/"


def new_figure():
    global fig_num
    if fig_num > 1:
        plt.tight_layout()
    fig = plt.figure(fig_num, figsize=(10, 6))
    fig_num += 1
    return fig


print("========================")
if len(sys.argv) > 1:
    data_path = sys.argv[1]
    fn_figure = sys.argv[2]
    show_plot = False
    should_save = True

    print("Ran from Node.js")
    print("Processing", data_path)
    print("Figure Filename:", fn_figure)
else:
    # no arguments, ran from pycharm pag dito
    data_path = "../ppg_test/ppg_test_data12"
    fn_figure = "ppg_leg_"
    show_plot = True
    should_save = True
    print("Ran from Pycharm")
    print("Processing", data_path)


# for fnum in file_nums:
# data_path = "../ppg_test/ppg_test_data" + str(fnum)
# fn_figure = "ppg_leg_"
# show_plot = True
subplot_loc = 311

# read input
f = open(data_path)
t, v = [], []
for line in f:
    entry = line.strip().split(',')
    x, y = entry
    t.append(int(x))
    v.append(int(y))

input_time = np.array(t)
input_value = np.array(v)

# plot input
new_figure()
plt.subplot(subplot_loc)
subplot_loc += 1
plt.title("Input Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(input_time, input_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

# print input properties
# T = abs(input_time[-1] - input_time[0]) / 1000.0
T = 5
N = len(input_time)
Fs = int(round(N / T))

print("========================")
print("Input Properties")
print("========================")
print("Duration: {}s | Number of Samples: {}".format(T, N))
print("Sampling Frequency: {}".format(Fs))


# PRE-PROCESSING
# interpolate input (500 samples)
interp_num = 500
fc = interp1d(input_time, input_value)
time = np.linspace(input_time[0], input_time[-1], num=interp_num)
interp_value = fc(time)

# print interpolated properties
# T = abs(time[-1] - time[0]) / 1000.0
T = 5
interp_N = len(time)
Fs = int(round(interp_N / T))

print("========================")
print("Interpolated Properties")
print("========================")
print("Duration: {}s | Number of Samples: {}".format(T, interp_N))
print("Sampling Frequency: {}".format(Fs))

# filter interpolated
# low pass
lp_sos = signal.butter(10, 5, 'lowpass', fs=Fs, output='sos')
lp_val = np.round(signal.sosfiltfilt(lp_sos, interp_value), 4)  # zero-phase

filtered_value = lp_val
# hp_sos = signal.butter(5, 1, 'highpass', fs=Fs, output='sos')
# filtered_value = np.round(signal.sosfiltfilt(hp_sos, lp_val), 4)

# amplify filtered
gain = 1
filtered_value *= gain

# plot filtered amplified
plt.subplot(subplot_loc); subplot_loc += 1
plt.title("Pre-processed Signal")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

# find systolic peaks
peaks, _ = signal.find_peaks(filtered_value)
peaks_diff = np.diff(peaks)
peaks_ave_diff = np.average(peaks_diff)
sys_distance = peaks_ave_diff * 0.75
peaks, _ = signal.find_peaks(filtered_value, distance=sys_distance)
peak_times = [time[p] for p in peaks]
peak_values = [filtered_value[p] for p in peaks]


print("========================")
print("Systolic Properties")
print("diff | ave diff | distance")
print(peaks_diff, peaks_ave_diff, sys_distance)


# get systolic points
systolic_points = peaks.tolist().copy()
systolic_times, systolic_values = [], []
for sp in systolic_points:
    systolic_times.append(time[sp])
    systolic_values.append(filtered_value[sp])

# plot systolic peaks
print(subplot_loc)
plt.subplot(subplot_loc)
plt.title("Initial Systolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(peak_times, peak_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))


# 2nd figure
# getting the diastolic points
grad1 = np.gradient(filtered_value) # * 30

max_fv = max(filtered_value)
max_grad1 = max(grad1)

gain_grad1 = max_fv / max_grad1

grad1 *= gain_grad1

print("Gradient Gain: ", gain_grad1)
print("min-max filtered:  ", min(filtered_value), max(filtered_value))
print("min-max gradient:  ", min(grad1), max(grad1))


grad1_peaks, _ = signal.find_peaks(grad1 * -1)
grad1_times = []
for g1p in grad1_peaks:
    grad1_times.append(time[g1p])


# interp signal local minima
yflip_filtered = filtered_value * -1
minima_points, _ = signal.find_peaks(yflip_filtered)

minima_diff = np.diff(minima_points)
minima_ave_diff = np.average(minima_diff)
dia_distance = minima_ave_diff * 0.75
minima_points, _ = signal.find_peaks(yflip_filtered, distance=dia_distance)

print("========================")
print("Diastolic Properties")
print("diff | ave diff | distance")
print(minima_diff, minima_ave_diff, dia_distance)

minima_times, minima_values = [], []
for lmp in minima_points:
    minima_times.append(time[lmp])
    minima_values.append(filtered_value[lmp])


print("ETO ETO")
print("Grad1 peaks:", grad1_peaks)
print("Minima points:", minima_points)

diastolic_points = []
for mp in minima_points:
    for g1p in grad1_peaks:
        if g1p >= mp:
            diastolic_points.append(g1p)
            break



print("diastolic points:", diastolic_points)
diastolic_times, diastolic_values = [], []
for dp in diastolic_points:
    diastolic_times.append(time[dp])
    diastolic_values.append(filtered_value[dp])

if should_save:
    print("========================")
    print("Figure 1 Saved...")
    plt.tight_layout()
    plt.savefig(save_dir + fn_figure + "fig1.svg", format="svg", bbox_inches='tight')

new_figure()
plt.subplot(311)
plt.title('Filtered Signal with Amplified 1st Derivative')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt_filtered, = plt.plot(time, filtered_value, label="Filtered")
plt_derivative, = plt.plot(time, grad1, color="g", linestyle="dashed", label="1st Derivative")
plt.legend(handles=[plt_filtered, plt_derivative])
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.axhline(0, color='gray', linestyle='dashed')


plt.subplot(312)
plt.title('Detected Filtered and First Derivative Minimas')
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(time, grad1, color="g", linestyle="dashed")
plt.plot(minima_times, minima_values, 'x', color="r")
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.axhline(0, color='gray', linestyle='dashed')

for g1t in grad1_times:
    plt.axvline(g1t, color='r', linestyle='dashed')


plt.subplot(313)
plt.title("Initial Diastolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.plot(diastolic_times, diastolic_values, 'x', color="r")


# systolic-diastolic peak matching
print("========================")
print("PEAK MATCHING")
print("Get points after reference point")
reference_point = minima_points[0]
print("reference_point", reference_point)
print("systolic_points")
print(systolic_points)
ref_systolic_points = [sp for sp in systolic_points if sp >= reference_point]
print(ref_systolic_points)

print("diastolic_points")
print(diastolic_points)
ref_diastolic_points = [dp for dp in diastolic_points if dp >= reference_point]
print(ref_diastolic_points)

print("Get systolic points after the first diastolic point on the left")
final_systolic_points = ref_systolic_points.copy()
if len(ref_diastolic_points) > 0:
    first_dp = ref_diastolic_points[0]
    final_systolic_points = [sp for sp in ref_systolic_points if sp > first_dp]

print("Get diastolic points before the last systolic point on the right")
final_diastolic_points = ref_diastolic_points.copy()
if len(ref_systolic_points) > 1:
    last_sp = ref_systolic_points[-1]
    final_diastolic_points = [dp for dp in ref_diastolic_points if dp < last_sp]

# get systolic peak time and values
final_systolic_times, final_systolic_values = [], []
for fsp in final_systolic_points:
    final_systolic_times.append(time[fsp])
    final_systolic_values.append(filtered_value[fsp])

# get diastolic peak time and values
final_diastolic_times, final_diastolic_values = [], []
for fsp in final_diastolic_points:
    final_diastolic_times.append(time[fsp])
    final_diastolic_values.append(filtered_value[fsp])

if should_save:
    print("========================")
    print("Figure 2 Saved...")
    plt.tight_layout()
    plt.savefig(save_dir + fn_figure + "fig2.svg", format="svg", bbox_inches='tight')


new_figure()
plt.subplot(211)
plt.title("Final Systolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(final_systolic_times, final_systolic_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# vertical line markers for systolic peaks
for spt in final_systolic_times:
    plt.axvline(spt, linestyle='--', color='gray')

plt.subplot(212)
plt.title("Final Diastolic Peaks")
plt.ylabel("ADC Value")
plt.xlabel("Time (ms)")
plt.plot(time, filtered_value)
plt.plot(final_diastolic_times, final_diastolic_values, 'x', color='red')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# vertical line markers for systolic peaks
for dpt in final_diastolic_times:
    plt.axvline(dpt, linestyle='--', color='gray')

# END
if should_save:
    print("========================")
    print("Figure 3 Saved...")
    plt.tight_layout()
    plt.savefig(save_dir + fn_figure + "fig3.svg", format="svg", bbox_inches='tight')


if show_plot:
    plt.show()



