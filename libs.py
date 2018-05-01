#helper functions
import os

def printLanes(spectrum, w, h):
    print('~'*h)
    for lane in sorted(spectrum):
        for s in range(w):
            print('~|'+(''.join(spectrum[lane]))+str(int(lane)))
    print('~'*h)

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

def updateLane(lane, newChar):#lane: arr, hit: string/char
    for i in range(len(lane)-1, 0, -1):
        lane[i] = lane[i-1]
    lane[0] = newChar
    return lane

def convert(ampl, high, thres):
    return (float(ampl-thres)/float(high-thres))

def clr():
    os.system('clear')
