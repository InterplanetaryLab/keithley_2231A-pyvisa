#!/bin/python3

from keithley_psu import keithley_psu

if __name__ == '__main__':
    psu = keithley_psu(device_str = "ASRL/dev/ttyUSB0::INSTR")
    psu.idn()
    psu.disable_output()
