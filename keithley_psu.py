import os.path
import serial
import sys
import time
import csv
import pyvisa

collect_file = "/home/ii-lab/keithley_test_scripts/data.csv"
last_collect_time_s = 0

arr_time = []
arr_data = []

# Keithley Power Supply interface class. Utilizes TTL to USB adapter to interface with. Could probably easily swapped to ethernet
class keithley_psu:
    def __init__(self, device_str, rm=None): 
        if (rm is None):
            self.rm = pyvisa.ResourceManager()
        else:
            self.rm = rm

        try:
            self.inst = self.rm.open_resource(device_str, baud_rate = 9600, data_bits = 8)
            self.inst.write_termination = '\n'
            self.inst.read_termination = '\n'
            self.inst.send_end = True
            self.inst.StopBits = 1
            idn_str = self.idn()
            if len(idn_str) > 1:
                # assuming device found.
                self.inst.write('SYST:REM')
            else:
                print("device not found")
        except:
            print("failed to open device")
    def idn(self): # returns the power supply's current set voltage
        idn_str = self.inst.query("*IDN?")
        print (idn_str)
        return idn_str
    def set_volt_all(self, volt_arr):
        cmd = "SOURCE:APPLY:VOLTAGE %0.2f,%0.2f,%0.2f"%(volt_arr[0],volt_arr[1],volt_arr[2])
        print(cmd)
        self.inst.write(cmd)
    def set_curr_all(self, curr_arr):
        cmd = "SOURCE:APPLY:CURRENT %0.2f,%0.2f,%0.2f"%(curr_arr[0],curr_arr[1],curr_arr[2])
        print(cmd)
        self.inst.write(cmd)
    def get_set_volt(self):
        cmd = "SOURCE:APPLY:VOLTAGE?"
        volt = self.inst.query(cmd)
        print(volt)
        volt = volt.split(",")
        data = []
        for i in volt:
            data.append(float(i))
        return data
    def get_current_volt(self,channel):
        cmd = "INSTRUMENT:NSELECT %d"%channel
        self.inst.write(cmd)
        cmd = "MEASURE:VOLTAGE?"
        self.inst.query(cmd)
        cmd = "FETCH:VOLTAGE?"
        data = self.inst.query(cmd)
        print(data)
        return float(data)
    def get_current_curr(self,channel):
        cmd = "INSTRUMENT:NSELECT %d"%channel
        self.inst.write(cmd)
        cmd = "MEASURE:CURRENT?"
        self.inst.query(cmd)
        cmd = "FETCH:CURRENT?"
        data = self.inst.query(cmd)
        print(data)
        return float(data)
    def get_set_curr(self):
        cmd = "SOURCE:APPLY:CURRENT?"
        curr = self.inst.query(cmd)
        print(curr)
        curr = curr.split(",")
        data = []
        for i in curr:
            data.append(float(i))
        return data
    def enable_output(self):
        self.enable_remote()
        self.inst.write("OUTP 1")
    def disable_output(self):
        self.enable_output()
        self.inst.write("OUTP 0")
    def disable_remote(self):
        self.inst.write("SYST:LOC")
    def enable_remote(self):
        self.inst.write("SYST:REM")
if __name__ == '__main__':
    psu = keithley_psu(device_str = "ASRL/dev/ttyUSB0::INSTR")
    psu.idn()
    psu.disable_output()
    psu.set_volt_all([10.5,9.5,4.5])
    psu.set_curr_all([0.5,1,2.0])
    psu.get_set_curr()
    psu.get_set_volt()
    psu.enable_output()
    psu.get_current_curr(2)
    psu.get_current_volt(3)
