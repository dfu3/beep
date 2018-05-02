
#TODO: adjust speed/delay of lanes

from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp
import time
import matplotlib.pyplot as plt

DELAY = 1
SYMB = '@'
LANE_W = 1
LANE_H = 50
CHUNK = 4096 # number of data points to read at a time
RATE = 150000#131072 #65536 #44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

thresholds = [
    2000000,
    #920000,
    900000,
    #750000,
    600000,
    #400000,
    200000,
    #350000,
    80000,
    #200000,
    50000,
    #75000,
    20000
    #20000
]
try:
    
    spectrum = dict()
    channels = dict()
    #amplAvgs = dict()
    #count = 0
    #update = False
    
    #init empty
    for i in range(len(thresholds)):
        target = 2**(i+6) #(2**float((i*.5)+6))
        if(i == len(thresholds)-1):
            target*=2
        spectrum[target] = [' ']*LANE_H
        channels[target] = thresholds[i]
        #amplAvgs[target] = 0

    #adjust thresholds
    adj = float(2.5) #% of OG
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

        #count+=1    
        for target in spectrum:
            ampl = fft[np.where(freq>target)[0][0]]
            #amplAvgs[target] += ampl
            #if(update):
            thres = channels[target]
            #avg = amplAvgs[target]/DELAY
            newChar = SYMB if(ampl > thres) else ' '
            spectrum[target] = updateLane(spectrum[target], newChar)
            #update = False
        
        #if(count >= DELAY):
        #    count = 0
        #    update = True
            
        clr()
        printLanes(spectrum, LANE_W, LANE_H)
        
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


