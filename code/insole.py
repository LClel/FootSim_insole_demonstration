import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from scipy import ndimage
import math
from scipy import interpolate
import scipy
from math import ceil, sqrt
from scipy import signal
import bz2
import _pickle as cPickle
import footsim as fs
from skimage.transform import resize
from copy import deepcopy

def get_foot_outline():
    """ Get the x and y coordinates relating the boundaries of the foot used within mapping

    Returns:
        x_outline (np.array): x coordinates
        y_outline (np.array): y coordinates

    """
    # Get foot boundary coordinates
    boundaries = fs.foot_surface.boundaries

    # turn coordinates from pixel space to foot space
    x_outline = []
    y_outline = []
    for i in range(len(boundaries)):
        for j in range(len(boundaries[i])):
            locs = fs.foot_surface.pixel2hand(np.array(boundaries[i][j]))
            x_outline = np.append(x_outline, locs[0])
            y_outline = np.append(y_outline, locs[1])

    return x_outline, y_outline

def import_data(filepath, **args):
    """ Reads a *.csv file with empirically recorded datapoints from a Tekscan Pressure Measurement System 7.00-22

    * UNITS KPa
    * SECONDS_PER_FRAME 0.01 (Per frame: ROWS 60 COLS 21)

    Args:
        filepath: filepath (str): path to the *.csv file
        **args:
            calibration_type (str): name of calibration type conducted
            extended_calibration (bool): True if extended calibration occurred, False if not
            frames (float): number of frames saved

    Returns:
        D (np.array()): 3D matrix of frames recorded

    """

    calibration_type = args.get('calibration_type', 'step')
    extended_calibration = args.get('extended_calibration', False)
    frames = args.get('frames', 2000)

    # Skips the heading of the data file and uses 61 lines per frame #
    if calibration_type == 'point':

        if extended_calibration == True:
            CSV = pd.read_csv(filepath, skiprows=34, header=None, nrows=frames * 61) # read in .csv file
            D_tmp = CSV.values
            D = D_tmp.reshape((-1, 61, 21,)).transpose(1, 2, 0)  # 3D matrix

        else:
            CSV = pd.read_csv(filepath, skiprows=33, header=None, nrows=frames * 61)
            D_tmp = CSV.values
            D = D_tmp.reshape((-1, 61, 21,)).transpose(1, 2, 0)  # 3D matrix


    else:
        CSV = pd.read_csv(filepath, skiprows=33, header=None,nrows=frames * 61)  # skiprows has to be different sometimes
        D_tmp = CSV.values
        D = D_tmp.reshape((-1, 61, 21,)).transpose(1, 2, 0)  # 3D matrix

    # cut off frame headers and convert to float

    D = D[0:-2, :, :]
    D[D == 'B'] = np.nan
    D = D.astype(float)

    return D

def cut_frame(D, calibrate, **args):
    """ Remove outer borders from pressure matrix

    Args:
        D (np.array): input data
        calibrate (bool): if True, will cut frame based on values within array. If False, will use pre-determined parameters entered through **args
        **args:
            min1 (int): index along the x axis where pressure starts
            min2 (int): index along the x axis where pressure finishes
            max1 (int): index along the y axis where pressure starts
            max2 (int): index along the y axis where pressure finishes

    Returns:

    """

    min2 = args.get('min2')
    max2 = args.get('max2')
    min1 = args.get('min1')
    max1 = args.get('max1')

    if calibrate == True:

        Dm = np.nanmean(D, axis=2)
        a1 = np.nanmax(Dm, axis=0)
        idx1 = np.where(a1 > 1) # find where pressure values are greater than 1
        if len(idx1[0]) != 0: # checks if pressure reaches the outer boundary of the matrix along the x axis
            min1 = np.min(idx1)
            max1 = np.max(idx1)
        else: # if pressure reaches the outer boundary of the matrix, use default min and max to cut data
            min1 = 0
            max1 = 20

        a2 = np.nanmax(Dm, axis=1)
        # find indexes where pressure value is greater than zero
        idx2 = np.where(a2 > 1)
        if len(idx2[0]) != 0: # checks if max pressure reaches the outer boundary of the matrix along the y axis
            min2 = np.min(idx2)
            max2 = np.max(idx2)
        else: # if max pressure reaches the outer boundary of the matrix, use default min and max to cut data
            min2 = 0
            max2 = 20

        # cut data and provide values to use to allow for consistent cutting for future data
        return D[min2:max2 + 1, min1:max1 + 1, :], min2, max2, min1, max1

    else:

        return D[min2:max2 + 1, min1:max1 + 1, :] # cut data

def map2footsim(D):
    """ Maps the pressures empirically recorded from a Tekscan Pressure Measurement System 7.00-22 into FootSim stimuli
    by changing the trace.

    Args:
        D (np.array): Pressure data processed with import_data() and cut_frame()

    Returns:
        s (FootSim Stimulus Object): contains sensor locations within s.locations
        regions (list): list of regions that relate to the sensor locations
        reshaped_data (2D np.array()): array containing only information from sensors that are used. Shape = (number of sensors, number of timepoints)
        idxs (list): list of integers relating to sensors mapped onto the foot
        D (np.array()): pressure matrix

    """

    dim = D.shape  # Dimensions of pressure data

    # get outline of the model foot
    x_outline, y_outline = get_foot_outline()

    cmin = [min(x_outline), min(y_outline)]
    cmax = [max(x_outline), max(y_outline)]

    # generate array of equally spaced coordinates between the minimum and maximum of the foot outline
    c0 = np.flip(np.linspace(cmin[1], cmax[1], dim[0]))
    c1 = np.linspace(cmin[0], cmax[0], dim[1])


    loc = np.zeros((0, 2)) # array to store sensor locations
    trace = np.zeros((0, dim[2])) # array to store pressure traces

    regions = []
    reshaped_data = np.zeros((0, dim[2]))
    m = 0
    idxs = []
    # loop through each point in the pressure matrix
    for i in range(dim[1]):

        for j in range(dim[0]):
            m += 1

            # coordinate of the sensor
            loca = np.array([c1[i], c0[j]])

            # identify region of the foot the sensor is located in
            region = fs.foot_surface.locate(loca)

            if region[0][0] == None:
                boundaries = fs.foot_surface.boundaries

                # turn coordinates from pixel space to foot space
                x_outline = []
                y_outline = []
                for i in range(len(boundaries)):
                    for j in range(len(boundaries[i])):
                        locs = fs.foot_surface.pixel2hand(np.array(boundaries[i][j]))
                        x_outline = np.append(x_outline, locs[0])
                        y_outline = np.append(y_outline, locs[1])

            if region[0][0] == '':
                # if the location is not on the foot, set values to zero
                D[j, i, :] = 0.0

            else:

                if np.isnan(D[j, i, 0]) or np.max(D[j, i, :]) == 0.0:
                    continue

                else:
                    # keep track of those locations in the pressure matrix that are mapped onto the foot
                    idxs.append(m - 1)

                    regions = np.append(regions, region[0][0]) # append region to list

                    # store pressures for all regions on the foot only
                    reshaped_data = np.vstack((reshaped_data, D[j, i, :]))

                    # save sensor location
                    loc = np.vstack((loc, loca))

                    # D is the 21 (columns per frame) x 61 (lines per frame) x 1794 (frames) 3D matrix from the dataset

                    # new calculation of indentation, using pressure, Young's modulus and Poisson's ratio
                    indent = fs.transduction.indentation(region=region[0][0], pressure=D[j, i, :].flatten())

                    # trace = np.vstack((trace, D[j, i, :].flatten()/129.0))
                    trace = np.vstack((trace, indent))

    # generate stimulus location
    s = fs.Stimulus(location=loc, trace=trace, fs=100, pin_radius=2.5)  # SENSEL_AREA 0.258064 cm2

    return s, regions, reshaped_data, idxs, D