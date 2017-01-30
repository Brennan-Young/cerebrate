import math
import random
import kafka

def nextTime(rateParameter):
    return -math.log(1.0 - random.random()) / rateParameter

def main():

    cluster = kafka.KafkaClient("52.33.229.60:9092")
    prod = kafka.SimpleProducer(cluster, async=False)

    topic = "my-topic"
    #msg_list = ["first message", "second message"]
    #prod.send_messages(topic, *msg_list)

    nodeCount = 1000
    consumeRate = 3 # a consumption event at rate 5
    produceRate = 1./10
    wType = "Poisson"
    dType = "AllConstant"
    Leader = 0
    t = 0

    if wType == "Poisson" and dType == "LeaderConstant":
        for i in range(100):
            flag = 0 
            t_last = t
            t = t + nextTime(consumeRate)
            if t % (1/produceRate) < t_last % (1/produceRate):
                # print(t)
                # print(t% 1/produceRate)
                # print(t_last)
                # print(t_last% 1/produceRate)
                print("Deposit at node "+ str(Leader) + " at time " + str(t - t%(1/produceRate)))
            n = random.randint(0,nodeCount-1)
            print("Request at node "+ str(n) + " at time "+str(t))
    elif wType == "Poisson" and dType == "AllConstant":
        for i in range(100):
            flag = 0 
            t_last = t
            t = t + nextTime(consumeRate)
            if t % (1/produceRate) < t_last % (1/produceRate):
                for n in range(nodeCount):
                    prod.send_messages(topic,*["Deposit at node "+ str(n) + " at time " + str(t - t%(1/produceRate)) + " aad"])
            n = random.randint(0,nodeCount-1)
            prod.send_messages(topic,*["Request at node "+ str(n) + " at time "+str(t) + " duck"])

if __name__=="__main__":
    main()