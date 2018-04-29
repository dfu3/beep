
#TODO: adjust speed/delay of lanes

from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp
import time
import matplotlib.pyplot as plt

SYMB = '#'
LANE_W = 2
LANE_H = 100
CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

thresholds = [
    950000,
    920000,
    880000,
    750000,
    575000,
    400000,
    375000,
    350000,
    275000,
    200000,
    137500,
    75000,
    47500,
    20000
]
try:
    
    spectrum = dict()
    channels = dict()
    #init empty
    for i in range(len(thresholds)):
        target = (2**float((i*.5)+6))
        spectrum[target] = [' ']*LANE_H
        channels[target] = thresholds[i]

    #adjust thresholds
    adj = float(1.0) #% of OG
    for val in thresholds:
        val *= adj
    
    clr()
    while(True):
        #read and process each sample
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] #nyquist 
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] #nyquist
        
        for target in spectrum:
            ampl = fft[np.where(freq>target)[0][0]]
            thres = channels[target]
            newChar = SYMB if(ampl > thres) else ' '
            spectrum[target] = updateLane(spectrum[target], newChar) 
            
        clr()
        #for lane in spectrum:
        #    print(lane)
        printLanes(spectrum, LANE_W, LANE_H)
        
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


