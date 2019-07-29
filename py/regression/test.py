import os
import wfdb
import wfdb.processing as proc


def download_files():
    wfdb.dl_database('bidmc', os.path.join(os.getcwd(), 'bidmc'))

def main():
    ppg_ch = 1
    ppg_record = wfdb.rdrecord('bidmc/bidmc01', sampto=3000, channels=[ppg_ch])

    ecg_ch = 4
    ecg_record = wfdb.rdrecord('bidmc/bidmc01', sampto=3000, channels=[ecg_ch])

    proc.gqrs_detect(d_sig=ecg_record.d_signal,
                     fs=ecg_record.fs,
                     adc_gain=ecg_record.adc_gain[0],
                     adc_zero=ecg_record.adc_zero[0])

    wfdb.plot_wfdb(ppg_record)
    wfdb.plot_wfdb(ecg_record)



if __name__ == '__main__':
    main()