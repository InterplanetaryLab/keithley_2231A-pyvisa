#!/bin/python3
from keithley_psu import keithley_psu

if __name__ == '__main__':
    psu = keithley_psu(device_str = "ASRL/dev/ttyUSB0::INSTR")
    psu.idn()
    psu.disable_output()
    psu.set_volt_all([12,0,0])
    psu.set_curr_all([.6,.1,.1])
    psu.enable_output()
