# -*- coding: utf-8 -*-

""" This example automatically finds the nearest GoDirect device
and starts reading measurements from the default sensor at
the typical data rate. Unlike the other examples that use the gdx module,
this example works directly with the godirect module. Take a look at 
the gdx getting started examples and the gdx.py file for more information.

Installation of the Python module:
# pip3 install godirect
"""

from godirect import GoDirect
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import os
import numpy as np
from gdx import gdx

def generate_graph(csvFile):
    df = pd.read_csv(csvFile, header=0)
    fig, ax = plt.subplots(figsize=(20,10))
    sns.lineplot(x=np.linspace(0,100,1000), y = df['Potential (V)'], ax=ax)
    filename = os.path.splitext(csvFile)[0]
    fig.savefig(f"{filename}.jpeg")

def main():
    # generate_graph('test1_3cm.csv')
    GDX = gdx() # new instance of gdx class
    GDX.open_usb() 
    GDX.select_sensors()

    with open('rubberband2.csv', 'w', newline='') as my_data_file:
    # The commented-out code below would be used if you want to hard-code in an absolute file path for the location of the csv file...
    #with open('C:/full/path/to/your/documents/folder/csvexample2.csv', 'w', newline='') as my_data_file:    
        csv_writer = csv.writer(my_data_file)
        GDX.start(period=10) 
        column_headers = GDX.enabled_sensor_info()
        csv_writer.writerow(column_headers)

        for i in range(0,1000):
            measurements = GDX.read() 
            if measurements == None: 
                break
            csv_writer.writerow(measurements)
            # print(measurements)

    GDX.stop()
    GDX.close()

    # # If you did not hard-code in an absolute path, this is where the file should be found.
    print("location of current working directory = ", os.getcwd())


main()


