import os.path
import serial
import sys
import time
import csv

com_port = "/dev/ttyUSB4"
collect_file = "/home/ii-lab/keithley_test_scripts/data.csv"
last_collect_time_s = 0

arr_time = []
arr_data = []

# Keithley Power Supply Logger Class. Utilizes TTL to USB adapter to interface with. Could probably easily swapped to ethernet
class keithley_psu:
    def __init__(self): 
        self.com_port = "/dev/ttyUSB1" # default port
    def get_current_curr(self):
        with serial.Serial(self.com_port, 9600, timeout=0.5) as ser:
            cmd = str.encode('MEAS:CURR? ALL'+'\n','utf-8')
            print( 'Sending:', cmd)
            ser.write(cmd)
            s = ser.read(256);
            data = []
            if len(s) > 0:
                print (s)
                s = s.decode()
                s_arr = s.split(",")
                if (len(s_arr) == 3):
                    for i in s_arr:
                        data.append(float(i))
                        print(float(i))
                    return data
            return []
    def get_current_volt(self):
        with serial.Serial(self.com_port, 9600, timeout=0.5) as ser:
            cmd = str.encode('MEAS:VOLT? ALL'+'\n','utf-8')
            print( 'Sending:', cmd)
            ser.write(cmd)
            s = ser.read(256);
            data = []
            if len(s) > 0:
                print (s)
                s = s.decode()
                s_arr = s.split(",")
                if (len(s_arr) == 3):
                    for i in s_arr:
                        data.append(float(i))
                        print(float(i))
                    return data
    def get_set_current(self,channel): # returns the power supply's current set current
        with serial.Serial(self.com_port, 9600, timeout=0.5) as ser:
            cmd = str.encode('INST:NSEL %d'%channel+'\n','utf-8')
            print( 'Sending:', cmd)
            ser.write(cmd)
            s = ser.read(256);
            cmd = str.encode('CURR?'+'\n', 'utf-8')
            ser.write(cmd)
            s = ser.read(256);
            data = []
            if len(s) > 0:
                print (s)
                return float(s)
    def get_set_volt(self,channel): # returns the power supply's current set voltage
        with serial.Serial(self.com_port, 9600, timeout=0.5) as ser:
            cmd = str.encode('*INST?'+'\n','utf-8')
            print( 'Sending:', cmd)
            ser.write(cmd)
            s = ser.read(256);
            data = []
            if len(s) > 0:
                print (s)
                return float(s)

if __name__ == '__main__':
    psu = keithley_psu()
    psu.com_port = "/dev/ttyUSB4"
    curr_volt_setting = psu.get_current_curr()
    for i in curr_volt_setting:
        print("curr: %f\n"%i)

    with open(collect_file, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        time_norm = time.time()
        writer.writerow(["Time (s)","Curr1 (A)","Curr2 (A)","Curr3 (A)"])
        while True:
            curr_volt_setting = psu.get_current_curr()
            timestamp = time.time()-time_norm
            writer.writerow(["%f"%timestamp,"%f"%curr_volt_setting[0],"%f"%curr_volt_setting[1],"%f"%curr_volt_setting[2]])
            time.sleep(1)





