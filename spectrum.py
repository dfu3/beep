
from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp
import time
import matplotlib.pyplot as plt

BAR_W = 1
BAR_H = 50
CHUNK = 4096 # number of data points to read at a time
RATE = 150000#44100 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# a change...

# another change

# yet another change

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
highs = [
    9500000,
    9200000,
    50000000, #wtf
    7500000,
    5750000,
    4000000,
    3750000,
    3500000,
    2750000,
    2000000,
    1375000,
    750000,
    475000,
    200000
]

try:
    ampRange = set()
    spectrum = dict()
    lastSample = dict()

    #adjust thresholds
    adj = float(.660) #% of OG
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
        
        for i in range(len(thresholds)):
            target = (2**float((i*.5)+6))
            thres = thresholds[i]
            ampl = fft[np.where(freq>target)[0][0]]
        
            if(ampl > highs[i]): highs[i] = ampl
                            
            if(ampl > thres):
                cleaned = convert(ampl, highs[i], thres)
                spectrum[target] = cleaned
                lastSample[target] = cleaned
            else:
                if(target in lastSample):
                    spectrum[target] = float(lastSample[target]*.9)
                else:
                    spectrum[target] = 0
               

        clr()
        printSpect(spectrum, BAR_W, BAR_H)

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


