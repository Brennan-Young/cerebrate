
'''
Script which generates data at random points in time simulating a Poisson process.
'''
import math
import random
import kafka
import time


def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def main():

    # Kafka information
    cluster = kafka.KafkaClient("localhost:9092")
    prod = kafka.SimpleProducer(cluster, async=False)
    topic = "my-topic"

    # Node information.  Currently hardcoded
    # TODO user should be able to specify a graph as an input to the problem
    nodeCount = 2

    # debugging
#    count = 0

    to = time.time()
    print(to)
    nT = nextTime(1)
    while(1):
        t = time.time()
        if t - to >= nT:
            to = t
#            count = count + 1

#            if count % 10000 == 0:
#                print("mark")
            nT = nextTime(10000)
            #print(nT)
            #print(str(int(round((to*100000)))))
            n = random.randint(0,nodeCount-1)
            prod.send_messages(topic,*[str(n) + ' ' + str(int(round((to*100000))))])

if __name__=="__main__":
    main()

