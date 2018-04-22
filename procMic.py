
from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
BASE = 900000 #initial sensitivity threshold
GROUPS = 8 #total number of frequency groups to visualize (starting at 64Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

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
        
        for i in range(GROUPS):

            target = (2**(i+6))
            thres = BASE-int( ((i*100000)+((target/((GROUPS-i)*5))*100)) )
            ampl = fft[np.where(freq>target)[0][0]]
            
            if(ampl > thres):
                cleaned = convert(ampl, thres, high, i+1)
                if( cleaned > high): high = cleaned
                if( cleaned < low): low = cleaned
                spectrum[target] = cleaned
            else:
                spectrum[target] = 0

        clr()
        pp.pprint(spectrum, width=1)
        print('Low: {}\nHigh: {}'.format(low, high))

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


