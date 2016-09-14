import glob
import os
import numpy as np
import data_loader as dl
import readInfo as ri


def save_data_arrays(folder_list):
    """
    This Function loops through a Data-set and extracts all important information needed to produce contour plots for
    analyzing the field geometry of the EOD. This function returns the folder-path where the processed data was saved.
    This function saves 5 numpy.arrays in the folder "./fieldgeo_arrays"
    :param folder_list: list of folders. Usually created using glob.glob()
    """
    res_path = './fieldgeo_arrays/'

    # Create empty lists to be filled later.
    x_pos = []
    y_pos = []
    conductivity = []
    recording_type = []  # 'Raster' or 'Line'
    amplitude = []

    for d in folder_list:

        print('\nAnalyzing data from: %s\n' % d)

        # Following try clause checks if there is an info.dat file inside the folder. If not, folder is excluded and
        # the code continues to the next folder.
        try:
            info = ri.read_info_file(d + '/info.dat')
        except:
            print('WARNING! No info.dat file located in %s. Proceeding with the next folder...' % d)
            continue

        x_position = info[0]['Recording:']['x-pos'][1:-4]
        y_position = info[0]['Recording:']['y-pos'][1:-4]
        leitfaehigkeit = info[0]['Recording:']['WaterConductivity']
        messtyp = info[0]['Recording:']['Comment']

        # Following try clause skips analyzing folders where there is no 'savetrace-EOD-1.dat' file.
        try:
            meta, t, eod = dl.load_eod_trace(d)
        except:
            continue

        std = np.std(eod, ddof=1) * 2.  # Calculate standard deviation of EOD-waveform (field-amplitude)

        # Fill the empty lists
        x_pos.append(x_position)
        y_pos.append(y_position)
        conductivity.append(leitfaehigkeit)
        recording_type.append(messtyp)
        amplitude.append(std)

    if not os.path.exists(res_path):
        os. makedirs(res_path)

    np.save(res_path + 'x_position.npy', np.array(x_pos))
    np.save(res_path + 'y_position.npy', np.array(y_pos))
    np.save(res_path + 'leitf.npy', np.array(conductivity))
    np.save(res_path + 'messtyp.npy', np.array(recording_type))
    np.save(res_path + 'amplitude.npy', np.array(amplitude))
    return res_path


if __name__ == '__main__':
    datensaetze = glob.glob('../data/feld_troubadix/*')

    result_path = save_data_arrays(datensaetze)

    print('\nField Geometry data successfully extracted. Arrays were created in %s\n' % result_path)