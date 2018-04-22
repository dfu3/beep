
from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp

BAR_W = 2
BAR_H = 100
CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
BASE = 900000 #initial sensitivity threshold
GROUPS = 8 #total number of frequency groups to visualize (starting at 64Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

thresholds = [

    950000,#64
    875000,#128
    725000,#256
    400000,#512
    350000,#1024
    200000,#2048
    75000,#4096
    20000#8192
]
highs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

try:
    ampRange = set()
    spectrum = dict()
    high = 0
    low = 0
    
    clr()
    while(True):
        #read and process each sample
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] #nyquist 
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] #nyquist

        lastTarg = 0   
        for i in range(len(thresholds)):
            target = (2**(i+6))
            thres = thresholds[i]
            high = highs[i]
            
            ampl = fft[np.where(freq>target)[0][0]]
            if( ampl > high): high = ampl
            
            if(ampl > thres):
                spectrum[target] = convert(ampl, high, thres)
            else:
                spectrum[target] = 0

        clr()
        printSpect(spectrum, BAR_W, BAR_H)
        #pp.pprint(spectrum, width=1)

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


