
from libs import *
import pyaudio
import numpy as np
import os
import pprint as pp

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)
TARGET = 8192 # frequency to single out
THRES = 20000 #sensitivity threshold (1,000,000 ~> 20,000)
SETUP_TIME = 100

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

try:
    ampRange = set()
    spectrum = dict()
    low= 0
    high = 0
    setup = 0

    clr()
    while(True): 
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] #nyquist 
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] #nyquist
        #assert freq[-1]>TARGET, "ERROR: increase chunk size"

        thres = 900000
        for i in range(8):
            target = 2**(i+6)
            thres-= (i*100000)
            ampl = fft[np.where(freq>target)[0][0]]
            if(ampl >= thres):
                if(setup < SETUP_TIME):
                    if( ampl < low): low = ampl
                    if( ampl > high): high = ampl
                    setup+=1
                    clr()
                    print('*SETUP*')
                else:
                    spectrum[target] = ampl

        #print spectrum
        clr()
        pp.pprint(spectrum, width=1)

        #ampl = fft[np.where(freq>TARGET)[0][0]] #<-OG            
        #if(ampl >= THRES): 
        #    ampRange.add(ampl)
        #    clr()
        #   print('ampl: {}'.format(ampl))
        #else:
        #    clr()
        #    print('out of range')
            
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    clr()
    #print('Amp Range: {}-->{}'.format(min(ampRange), max(ampRange)))
    pass


