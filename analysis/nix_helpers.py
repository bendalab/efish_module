import nixio as nix
import numpy as np
import os
from IPython import embed


def nix_metadata_to_dict(section):
    info = {}
    for p in section.props:
        info[p.name] = [v.value for v in p.values]
    for s in section.sections:
        info[s.name] = nix_metadata_to_dict(s)
    return info


def read_eod(data_file, duration=10):
    """ Reads the recorded EOD from the given nix file.

    :param data_file: The path of the nix file.
    :param duration: the duration of the segment that should be read. Default is 10 s.
    :return time: numpy vector containing the time
    :return eod: numpy vector containing the eod signal.
    """
    if not os.path.exists(data_file):
        return None
    f = nix.File.open(data_file, nix.FileMode.ReadOnly)
    b = f.blocks[0]
    eod_array = b.data_arrays["EOD"]
    sample_rate = 1./eod_array.dimensions[0].sampling_interval
    max_index = duration * sample_rate
    max_index = int(eod_array.shape[0] if max_index > eod_array.shape[0] else max_index)
    eod = eod_array[:max_index]
    time = np.asarray(eod_array.dimensions[0].axis(max_index))
    f.close()
    return time, eod


def read_eod_events(data_file):
    """ Reads the recorded EOD events from the nix file.

    :param data_file: the path of the nix file.
    :return the event times.
    """
    if not os.path.exists(data_file):
        return None
    f = nix.File.open(data_file, nix.FileMode.ReadOnly)
    b = f.blocks[0]
    events_array = b.data_arrays['EOD_events']
    times = events_array[:]
    f.close()
    return times


def read_subject_info(data_file):
    """ Reads the subjects information from the metadata.

    :param data_file: The path of the nix file.
    :return the subject information as a dictionary.
    """
    if not os.path.exists(data_file):
        return None
    dataset_stub = data_file.split('/')[-1].split('.')[0]
    f = nix.File.open(data_file, nix.FileMode.ReadOnly)
    b = f.blocks[0]
    m = b.metadata
    subject_m = m['Subject-' + dataset_stub]
    subject_info = nix_metadata_to_dict(subject_m)
    f.close()
    return subject_info


def read_block_metadata(data_file):
    """ Reads all metadata from the given nix file.

    :param data_file: the path of the nix file.
    :return metadata: a dictionary containing all metadata.
    """
    if not os.path.exists(data_file):
        return None
    f = nix.File.open(data_file, nix.FileMode.ReadOnly)
    b = f.blocks[0]
    m = b.metadata
    metadata = nix_metadata_to_dict(m)
    f.close()
    return metadata


def read_df(data_file):
    if not os.path.exists(data_file):
        print("File not found %s" % data_file)
        return -9999
    df = -9999
    before = -9999
    after = -9999
    duration = -9999
    with open(data_file, 'r') as tf:
        lines = tf.readlines()
    for l in lines:
        if "#" not in l and len(l.strip()) > 0:
            break
        if "delta f" in l.lower():
            df = float(l.split(":")[-1].strip()[:-2])
        if "before" in l.lower():
            val = l.split(':')[-1].strip()
            before = float(val[:val.index('s')])
        if "after" in l.lower():
            val = l.split(":")[-1].strip()
            after = float(val[:val.index('s')])
        if "duration" in l.lower():
            val = l.split(":")[-1].strip()
            duration = float(val[:val.index('s')])
    return df, before, after, duration


def read_jar_data2(data_file, count=-1):
    if not os.path.exists(data_file):
        print("File  not found %s!" % data_file)
        return None, None

    dfs = []
    data = []
    path = data_file[:data_file.rindex('/')]
    f = nix.File.open(data_file, nix.FileMode.ReadOnly)
    b = f.blocks[0]
    tag = None

    for i, tag in enumerate(b.multi_tags):
        if "ManualJAR" in tag.name:
            number = int(tag.name.split('-')[-1])
            number = str(number) if number > 9 else "0%i" % number
            jar_file_name = "%s/manualjar-eod-%s.dat" % (path, number)
            if os.path.exists(jar_file_name):
                df, before, after, duration = read_df(jar_file_name)
            start_time = tag.positions[:][0]
            duration = tag.extents[:][0]
            events_array = b.data_arrays['EOD_events']
            times = events_array[:]
            eod_times = times[(times > (start_time - before)) & (times < (start_time + duration + after))] - start_time

            data.append(eod_times)
            dfs.append(df)

            if count > -1 and i >= (count-1):
                break
        tag = None
    f.close()
    return data, dfs


def read_jar_data(data_file, pre_stimulus_duration=5., post_stimulus_duration=20):
    """
    Liest die Daten von einem JAR Experiment.

    :param data_file:
    :param pre_stimulus_duration: Zeit bevor der Stimulus an war.
    :param post_stimulus_duration:  Zeit nachdem der Stimulus aus war.
    :return: pre_stimulus_duration: die wirklich vor dem Stimulus ausgelesene Zeit.
             post_stimulus_duration: die tatsaechlich nach dem Stimulus ausgelesene Zeit.
             duration: die Dauer der Stimulation
             eod: die EOD in dem angegebenen Zeitraum
             eod_times: die  ZEitpunkte der detektieren EODs
             time: ein Zeitvektor, gleiche Laenge, wie eod
             metadata: dictionary mit allen Metadaten

    """
    if not os.path.exists(data_file):
        return None
    f = nix.File.open(data_file, nix.FileMode.ReadOnly, backend="hdf5")
    b = f.blocks[0]
    m = b.metadata
    metadata = nix_metadata_to_dict(m)
    tag = None

    for t in b.multi_tags:
        if "ManualJAR" in t.name:
            tag = t
            break

    stim_meta = nix_metadata_to_dict(tag.metadata)
    metadata.update(stim_meta)

    start_time = tag.positions[:][0]
    duration = tag.extents[:][0]
    events_array = b.data_arrays['EOD_events']
    eod_array = b.data_arrays["EOD"]
    sampling_rate = 1./eod_array.dimensions[0].sampling_interval

    pre_stimulus_duration = pre_stimulus_duration if start_time > pre_stimulus_duration else tag.positions[:][0]
    if (start_time + duration + post_stimulus_duration) * sampling_rate > len(eod_array):
        post_stimulus_duration = len(eod_array) / sampling_rate - start_time - duration
    end_time = start_time + duration + post_stimulus_duration

    start_index = (start_time - pre_stimulus_duration) * sampling_rate
    end_index = end_time * sampling_rate

    eod = eod_array[:][int(start_index):int(end_index)]
    times = events_array[:]
    eod_times = times[(times > (start_time - pre_stimulus_duration)) & (times < end_time)] - start_time
    f.close()
    time = np.arange(len(eod)) / sampling_rate - pre_stimulus_duration
    return pre_stimulus_duration, post_stimulus_duration, duration, eod, eod_times, time, metadata


if __name__ == "__main__":
    # make sure to close the file before exiting! Take care, when using embed!
    datafile = '/Users/jan/zwischenlager/efish_kurs/data/chirps/2017-11-27-aa-amnesix/2017-11-27-aa-amnesix.nix'
    # t,e = read_eod(datafile)
    # events = read_eod_events(datafile)
    # info = read_subject_info(datafile)
    # b_info = read_block_metadata(datafile)
    data, dfs = read_jar_data2(datafile)
    embed()
