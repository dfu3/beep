import time
from libs import *

thresholds = [
    950000,#64
    900000,#128
    750000,#256
    400000,#512
    350000,#1024
    200000,#2048
    75000,#4096
    20000 #8192
]

last = 0
for i in range(len(thresholds)):
    if(i != 0):
        print(last)
        mid = (last + thresholds[i])/2
        last = thresholds[i]
        print(mid)
