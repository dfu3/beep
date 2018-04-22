#helper functions
import os

def convert(ampl, high, thres):
    return int( (float(ampl-thres)/float(high))*10)

def clr():
    os.system('clear')
