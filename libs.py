#helper functions
import os

def printSpect(spectrum, w, h):
    print('--')
    for freq in sorted(spectrum):
        bars = spectrum[freq]
        for s in range(w):
            bar = ('#'*int(bars*h))
            if(freq <= 128): print('L |{}'.format(bar))
            elif(freq <= 2048): print('M |{}'.format(bar))
            else: print('H |{}'.format(bar))
    print('--')

def convert(ampl, high, thres):
    return (float(ampl-thres)/float(high-thres))

def clr():
    os.system('clear')
