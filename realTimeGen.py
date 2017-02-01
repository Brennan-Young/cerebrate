
'''
Script which generates data at random points in time simulating a Poisson process.
'''
import math
import random
import kafka
import time


def nextTime(rateParameter):
    ''' 
    Function which generates a new random time as the next arrival time in a Poisson process
    '''
    return -math.log(1.0 - random.random()) / rateParameter

def nextTimeSineDemand(rateParameter, sinePeriod, currentPeriodLocation):
    '''
    Function which generates a new random time as the next arrival time in a Poisson process.  The paramater of the Poisson process varies according to a sinusoid.  
    '''
    l = range(sinePeriod)
    lLen = len(l)
    s = [ ( ( math.sin(2 * math.pi * x / lLen )) * 1/2 + 1 ) for x in l ]
    nextPeriodLocation = (currentPeriodLocation + 1) % sinePeriod
    nextParam = rateParameter * s[currentPeriodLocation]
    return nextParam, nextPeriodLocation

def main():

    # Kafka information
    cluster = kafka.KafkaClient("localhost:9092")
    prod = kafka.SimpleProducer(cluster, async=False)
    topic = "my-topic"

    # Node information.  Currently hardcoded
    # TODO user should be able to specify a graph as an input to the problem
    nodeCount = 2

    # Parameter generation information
    generationType = "sine"
    avgRate = 100
    sineLength = 500

    # debugging
#    count = 0

    to = time.time()
    print(to)
    if generationType == "sine":
        periodLocation = 0
        nextParam, periodLocation = nextTimeSineDemand(avgRate, sineLength, periodLocation)
        nT = nextTime(nextParam)
    else:
        nT = nextTime(1)
    while(1):
        t = time.time()
        if t - to >= nT:
            to = t
#            count = count + 1

#            if count % 10000 == 0:
#                print("mark")
            if generationType == "sine":
                nT = nextTime(nextParam)
                nextParam, periodLocation = nextTimeSineDemand(avgRate, sineLength, periodLocation)
                #print(nextParam)
            else:
                nT = nextTime(10000)
            #print(nT)
            #print(str(int(round((to*100000)))))
            n = random.randint(0,nodeCount-1)
            prod.send_messages(topic,*[str(n) + ' ' + str(int(round((to*1000))))])

if __name__=="__main__":
    main()

