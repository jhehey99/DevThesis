import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# TODO SAVEDIR IS /files/bos/record_id_[ir, red].svg
fig_num = 1
save_dir = "../_files/"
fn_suffix = ["ir", "red"]

def new_figure():
    global fig_num
    if fig_num > 1:
        plt.tight_layout()
    fig = plt.figure(fig_num, figsize=(10, 6))
    fig_num += 1
    return fig


print("========================")
if len(sys.argv) > 1:
    data_paths = [sys.argv[1], sys.argv[2]]
    save_dir = sys.argv[3]
    show_plot = False
    should_save = True

    print("Ran from Node.js")
    print("Processing", data_paths)
else:
    # no arguments, ran from pycharm pag dito
    data_paths = ["bos_ir2", "bos_red2"]
    show_plot = True
    should_save = True
    print("Ran from Pycharm")


# get time, value pairs as numpy array from given path
def get_data_pairs(path):
    f = open(path)
    t, v = [], []
    for line in f:
        entry = line.strip().split(',')
        x, y = entry
        t.append(int(x))
        v.append(int(y))

    it = np.array(t)
    iv = np.array(v)
    return [it, iv]


# set to input_data
IR, RED = 0, 1
TIME, VALUE = 0, 1
input_data = [get_data_pairs(path=path) for path in data_paths]

# INPUT SIGNAL MATCHING
time_delay = 300 # ms
red_times, red_values = input_data[RED]
key_time, key_index = red_times[0], 0

# find the index where signal has settled
for i, pair in enumerate(zip(red_times, red_values)):
    time, value = pair
    if value == 0:
        key_time = time

    if time >= (key_time + time_delay):
        key_index = i
        break

# get data points after the key index
input_data[RED][TIME] = np.array(input_data[RED][TIME][key_index:])
input_data[RED][VALUE] = np.array(input_data[RED][VALUE][key_index:])
input_length = len(input_data[RED][TIME])

# get same length from ir signal or + 1 data point
ir_length = len(input_data[IR][TIME])
if ir_length > input_length:
    len_diff_half = (ir_length - input_length) // 2
    input_data[IR][TIME] = np.array(input_data[IR][TIME][len_diff_half:ir_length - len_diff_half])
    input_data[IR][VALUE] = np.array(input_data[IR][VALUE][len_diff_half:ir_length - len_diff_half])


# PROCESSING
figures = []
AC, DC = 0, 1
ir_components, red_components = [], []

for dpi, data in enumerate(input_data):
    print("Processing", "IR" if dpi == 0 else "RED")
    input_time, input_value = data
    subplot_loc = 411

    # plot input
    fig = new_figure()
    figures.append(fig)
    plt.subplot(subplot_loc)
    subplot_loc += 1
    plt.title(("IR LED " if dpi == 0 else "RED LED ") + "Input Signal")
    plt.ylabel("ADC Value")
    plt.xlabel("Time (ms)")
    plt.plot(input_time, input_value)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    T = 5
    interp_N = len(input_time)
    Fs = int(round(interp_N / T))

    # low pass
    lp_sos = signal.butter(10, 5, 'lowpass', fs=Fs, output='sos')
    lp_val = np.round(signal.sosfiltfilt(lp_sos, input_value), 4)  # zero-phase
    filtered_value = lp_val

    # plot filtered amplified
    plt.subplot(subplot_loc); subplot_loc += 1
    plt.title("Pre-processed Signal")
    plt.ylabel("ADC Value")
    plt.xlabel("Time (ms)")
    plt.plot(input_time, filtered_value)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))


    # prominence finding
    peaks, _ = signal.find_peaks(filtered_value)
    prominences = signal.peak_prominences(filtered_value, peaks)[0]

    # ac component finding
    prom_ave_half = np.average(prominences) / 2
    ac_points = [peaks[i] for i, prominence in enumerate(prominences) if prominence > prom_ave_half]
    ac_components = [prominence for prominence in prominences if prominence > prom_ave_half]

    # dc component finding
    inverted_values = filtered_value * -1
    inverted_peaks, _ = signal.find_peaks(inverted_values)

    # get dc components after each ac component
    dc_points = []
    dc_idx = 0
    for ac_pk in ac_points:
        while dc_idx < len(inverted_peaks) and inverted_peaks[dc_idx] < ac_pk:
            dc_idx += 1

        if dc_idx < len(inverted_peaks):
            dc_points.append(inverted_peaks[dc_idx])


    # ac-dc component matching
    reference_point = dc_points[0]

    print("Get ac points after the first dc point on the left")
    fin_ac_points, fin_ac_components = [], []
    if len(dc_points) > 0:
        first_dc = dc_points[0]
        # get indices of ac points in ref_ac_point
        ac_indices = [i for i in range(len(ac_points)) if ac_points[i] > first_dc]
        fin_ac_points = [ac_points[i] for i in ac_indices]
        fin_ac_components = [round(ac_components[i], 4) for i in ac_indices]

    print("Get dc points before the last ac point on the right")
    fin_dc_points = []
    if len(fin_ac_points) > 1:
        last_ac = fin_ac_points[-1]
        fin_dc_points = [dcp for dcp in dc_points if dcp < last_ac]


    # get ac and dc component time and values
    fin_ac_times, fin_ac_values = input_time[fin_ac_points], filtered_value[fin_ac_points]
    fin_ac_min = fin_ac_values - fin_ac_components
    fin_dc_times, fin_dc_components = input_time[fin_dc_points], filtered_value[fin_dc_points]

    # store the components
    if dpi == 0:
        ir_components.append(fin_ac_components)
        ir_components.append(fin_dc_components)
    else:
        red_components.append(fin_ac_components)
        red_components.append(fin_dc_components)


    # plotting ac and dc components
    plt.subplot(subplot_loc);
    subplot_loc += 1
    plt.title("AC Components")
    plt.plot(input_time, filtered_value)
    plt.plot(fin_ac_times, fin_ac_values, 'x', color='g')
    plt.plot(fin_ac_times, fin_ac_min, 'x', color='r')
    plt.vlines(x=fin_ac_times, ymin=fin_ac_min, ymax=fin_ac_values)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    plt.subplot(subplot_loc);
    subplot_loc += 1
    plt.title("DC Components")
    plt.plot(input_time, filtered_value)
    plt.plot(fin_dc_times, fin_dc_components, 'x', color='r')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.tight_layout()


    # saving the figure
    if should_save:
        filename = save_dir + "_" + fn_suffix[dpi] + ".svg"
        plt.tight_layout()
        plt.savefig(filename, format="svg", bbox_inches='tight')
        print("========================")
        print(filename, "Saved...")




# Components are found
print("ir_components", ir_components)
print("red_components", red_components)

# get average from each components
ir_ac_ave = np.round(np.average(ir_components[AC]), 4)
ir_dc_ave = np.round(np.average(ir_components[DC]), 4)
ir_ratio = np.round(ir_ac_ave / ir_dc_ave, 4)
print("IR: AC ave =", ir_ac_ave, " | DC ave =", ir_dc_ave, " Ratio =", ir_ratio)

red_ac_ave = np.round(np.average(red_components[AC]), 4)
red_dc_ave = np.round(np.average(red_components[DC]), 4)
red_ratio = np.round(red_ac_ave / red_dc_ave, 4)
print("RED: AC ave =", red_ac_ave, " | DC ave =", red_dc_ave, " Ratio =", red_ratio)

ir_red_ratio = np.round(ir_ratio / red_ratio, 4)
print("IR/RED Ratio =", ir_red_ratio)




if show_plot:
    plt.show()











































