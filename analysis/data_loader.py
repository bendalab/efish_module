from pyrelacs.DataClasses import load
import numpy as np
import scipy.signal as signal


def load_data(filename):
    """ This function loads a RELACS's .dat file and extract the meta-data, keys and the actual data.

    :param filename: the
    :return: Three lists of dictionaries. The first list contains the meta-data, the second the keys and the third
    contains the data. Need to call the dictionaries with valid keys to access desired data.
    """
    data_loader = load(filename)
    meta_data, key, raw_data = data_loader.selectall()
    data = []
    for i in range(len(raw_data)):
        temp = {}
        column_names = []
        for k in key[0]:
            column_names.append(k[0])
            temp[k[0]] = []
        for line in raw_data[i]:
            line_parts = line.strip().split()
            for c, p in zip(column_names, line_parts):
                temp[c].append(float(p))

        for k in temp.keys():
            temp[k] = np.asarray(temp[k])
        data.append(temp)
    return meta_data, key, data

def load_eod_trace(folder_path):

    """ Loads the meta-data, time-trace and EOD-trace of a RELACS 'savetrace-EOD-1.dat' file.

    :param folder_path: String. Path to desired folder containing the data.
    :return: Returns three variables. The first one is a dictionary containing the meta-data. The second variable
    returns a numpy.array with the time-trace. The third variable returns a numpy.array with the EOD-trace.
    """
    if folder_path[-1] != '/':  # check if folder_path ends with '/'
        folder_path += '/'

    meta_data, k, data = load_data(folder_path + 'savetrace-EOD-1.dat')

    t = data[0]['t']
    eod_trace = data[0]['EOD']

    return meta_data[0], t, eod_trace


def load_manual_jar(data_file, sampling_rate=10000, filter_cutoff=0.):
    """
    Load data from manualjar files.

    :param data_file: The filename of the data file.
    :param sampling_rate: the desired sampling rate of the returned trace. Default = 10000
    :param filter_cutoff: Cutoff frequency of a a low-pass filter. Default 0, i.e. no filter
    :return: the difference frequency, the eod frequency of the animal, the time recorded before stimulus onset, the
    recording time after stimulus offset, the stimulus duration, the time axis and the frequency as a function of time.
    """
    meta_data, k, data = load_data(data_file)
    df = meta_data[0]['Delta f']
    eodf = meta_data[0]['EODf']
    time = data[0]['time']
    freq = data[0]['freq']

    before = meta_data[0]['Settings']['before']
    after = meta_data[0]['Settings']['after']
    duration = meta_data[0]['Settings']['duration']

    b = float(before[:-7])
    a = float(after[:-7])
    d = float(duration[:-7])
    time_axis = np.arange(-b, a + d, 1./sampling_rate)
    response = np.interp(time_axis, time, freq)
    if filter_cutoff > 0.:
        b, a = signal.butter(2, float(filter_cutoff)/sampling_rate, 'low')
        response = signal.filtfilt(b, a, response)
    return df, eodf, before, after, duration, time_axis, response


def load_eod_times(folder_path):

    """ Loads the meta-data, the times and the amplitude of events of a RELACS 'saveevents-EOD-1.dat' file.

    :param folder_path: String. Path to desired folder containing the data.
    :return: Returns three variables. The first one is a dictionary containing the meta-data. The second variable
    returns a numpy.array with the times of the recorded events. The third variable returns a numpy.array with the
    recorded Amplitude of each event.
    """
    if folder_path[-1] != '/':  # check if folder_path ends with '/'
        folder_path += '/'

    data_loader = load(folder_path + "/saveevents-EOD-1.dat")
    meta_data, key, raw_data = data_loader.selectall()

    if len(key) == 1:
        t = raw_data[0]
        return meta_data[0], t
    else:
        t = raw_data[0]
        event_ampl = raw_data[1]
        return meta_data[0], t, event_ampl