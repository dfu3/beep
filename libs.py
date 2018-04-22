#helper functions
import os

def convert(ampl, thres, upper, scale):
    return int((ampl-thres)/(10.0/scale))

def clr():
    os.system('clear')
