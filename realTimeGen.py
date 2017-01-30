
import math
import random
import kafka
import time


def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def main():
    f = open('test.out','w')
    to = time.time()
    nT = nextTime(1)
    print(nT)
    while(1):
        t = time.time()
        if t - to > nT:
            to = time.time()
            nT = nextTime(100000)
            f.write(str(to) + '\n')

    f.close()
if __name__=="__main__":
    main()