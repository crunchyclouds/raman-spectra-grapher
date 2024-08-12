import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
import warnings
import time
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import matplotlib

#main function for the graphing of raman spectra data

#input folder
folder=r"D:\Data\Raman\0802"

#identifying csv files within the folder
files = [file for file in pathlib.Path(folder).glob("*.csv")]

#correcting matplotlib presets
matplotlib.rcParams.update({'font.size': 18})

#removing temporary files
for file in files:
    if "~" in str(file):
        files.remove(file)

#looping through all files
for file in files:

    #updating user of status
    print(f'Reading from {file}')
    print('Processing your files...')

    #reading excel data for cycle index and current capacity
    df = pd.read_csv(file, header=105)

    y_axis = df['Dark Subtracted #1'] - df['RelativeIntensityCorrection_Ratio #1']
    x_axis = df['Raman Shift']

    #correcting for series height and stacking


    #creating a plot
    series = str(pathlib.Path(file).stem)
    #plt.xlim(400,675)
    plt.ylim(0,20000)
    plt.plot(x_axis, y_axis,
             marker='',
             label=series)
    plt.legend(loc='lower right')

    n=1
    stack=0
    print(f'Data set {n}/{len(files)} complete.')
    n+=1
    stack+=4000

#assigned constant values
plt.ylabel(r"Intensity (a.u.)")
plt.xlabel("Raman Shift (cm^-1)")
plt.title(str(pathlib.Path(folder).stem))
plt.show()