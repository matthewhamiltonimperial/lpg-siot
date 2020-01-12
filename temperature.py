import os
import glob
import time
from ISStreamer.Streamer import Streamer
import csv

streamer = Streamer(bucket_name="Temperature Stream", bucket_key="XXXXXXXXXXx", access_key="XXXXXXXXXXXXXXXXXXXXXXXXXX") # Removed for security
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'



def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def store_data(temperature):
    append = [temperature]
    with open('day_data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(append)
    csvFile.close()
    print("data stored")

while True:
    temp_c = read_temp()
    store_data(temp_c)
    streamer.log("temperature (C)", temp_c)
    print("reading complete")
    time.sleep(19)
