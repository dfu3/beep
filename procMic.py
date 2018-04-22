
from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
BASE = 900000 #initial sensitivity threshold
SETUP_TIME = 100

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

try:
    ampRange = set()
    spectrum = dict()
    high = 0

    clr()
    while(True):
        #read and process each sample
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] #nyquist 
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] #nyquist
        
        for i in range(8):

            target = 2**(i+6)
            thres = BASE-(i*100000)
            ampl = fft[np.where(freq>target)[0][0]]
            
            if(ampl >= thres):
                if( ampl > high): high = int(ampl)
                spectrum[target] = int(ampl)
            else:
                spectrum[target] = 0

        clr()
        pp.pprint(spectrum, width=1)

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    pass


