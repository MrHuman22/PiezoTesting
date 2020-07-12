from godirect import GoDirect
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import os
import numpy as np
from gdx import gdx
import typing
import PySimpleGUI as sg
from enum import Enum
from datetime import datetime
from time import sleep

testpath = os.path.join(os.getcwd(),'MagTests')

# TODO: validation on filenames

class GuiKeys(Enum):
    filename = 'filename'
    test_details = 'test_details'
    quit_program = 'Quit'
    cancel = 'Cancel'
    submit = 'Submit'

def get_timestamp() -> str:
    return datetime.strftime(datetime.now(),"%Y-%m-%d_%H-%M")

def countdown() -> None:
    print('Ready!')
    sleep(1)
    print('Set!')
    sleep(1)
    print('Go!')

def run_test(csv_filepath: str) -> None:
    GDX = gdx()
    GDX.open_usb()
    GDX.select_sensors([1]) # now will automatically select the corret sensor
    print(f"Writing to {csv_filepath}")
    with open(csv_filepath, 'w', newline='') as target_file:
        writer = csv.writer(target_file)
        GDX.start(period=10)
        column_headers = GDX.enabled_sensor_info()
        writer.writerow(column_headers)
        countdown()
        for i in range(0, 1000):
            measurements = GDX.read()
            if measurements == None:
                break
            else:
                writer.writerow(measurements)
    GDX.stop()
    GDX.close()
    print("Finishing up with the sensor")

def create_multi_graph(csv_filepath: str, test_details: str = '') -> None:
    print("Now starting to graph it...")
    df = pd.read_csv(csv_filepath, header=0)
    y_values = df['Potential (V)']
    f = plt.figure(figsize=(20,10))
    gs = gridspec.GridSpec(1,2,width_ratios=[10,1])
    ax1 = plt.subplot(gs[0])
    ax1.set_title(f"{test_details} (sampled every 10ms)")
    ax1.set_xlabel('Seconds')
    ax1 = sns.lineplot(x=np.linspace(0,10,1000), y = y_values)
    ax2 = plt.subplot(gs[1],sharey=ax1)
    ax2.set_title("Violin plot of voltages")
    ax2.set_ylabel('Potential (V)')
    ax2 = sns.violinplot(y=y_values, orient='v')
    plot_filepath = csv_filepath[:-4]+".png"
    print(f"Saving plot to {plot_filepath}")
    plt.savefig(plot_filepath, bbox_inches='tight')
    

def create_graph(csv_filepath: str, test_details: str = '') -> None:
    df = pd.read_csv(csv_filepath, header=0)
    fig, ax = plt.subplots(figsize=(20,10))
    ax.set_title(f"{test_details} (sampled every 10ms)")
    ax.set_xlabel('Seconds')
    x_values = np.linspace(0,10,1000)
    y_values = df['Potential (V)']
    sns.lineplot(x=x_values, y = y_values)
    plot_filepath = csv_filepath[:-4]+".png"
    plt.savefig(plot_filepath, bbox_inches='tight')
    plt.show() # Comment out to stop auto-show

def generateLayout() -> list:
    return [[sg.Text("Enter file name: "), sg.InputText(key=GuiKeys.filename.value, size=(8,1)), sg.Text(".csv")],
        [sg.Text("Test Details: "), sg.InputText(key=GuiKeys.test_details.value)],
        [sg.Submit(),sg.Cancel(),sg.Quit()]]

def main() -> None:
    print('Looping...')
    window = sg.Window("Choose filename", layout=generateLayout()) 
    event, values = window.read()
    if event == GuiKeys.quit_program.value:
        print("Ending the program.")
        return
    elif event in (GuiKeys.cancel.value,None):
        print("Operation cancelled. Restarting Loop.")
        window.close()
        return
    elif event == GuiKeys.submit.value:
        filename = values[GuiKeys.filename.value]+'.csv'
        filepath = os.path.join(testpath,f"{get_timestamp()}_{filename}")
        test_details = values[GuiKeys.test_details.value]
        run_test(filepath)
        # create_multi_graph(filepath,test_details=test_details)
        create_graph(filepath,test_details=test_details)
    else:
        print("Unknown input!")
    window.close()
    window = None
    filepath = None # wipe the filepath
    # print("Restarting Loop.")
    # img = Image.open(r"Tests")

if __name__ == "__main__":
    main()
