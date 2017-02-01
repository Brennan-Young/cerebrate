import rethinkdb as r
import numpy
import matplotlib.pyplot as plt

r.connect( "35.163.48.63", 28015).repl()
#cursor = r.table("test3").run()
#r.table("cumulativeTest2").index_create("timeStamp").run()
cursor = r.table("cumulativeTest2").order_by(index="timeStamp").filter(r.row["nodeID"] == 1).run()
# cursor = r.table("cumulativeTest2").filter(r.row["nodeID"] == 0).run()

#for document in cursor:
 #   print(document["timeStamp"])

l = [(document["timeStamp"],document["requestCount"])for document in cursor]
x = [a[0] for a in l]
y = [a[1] for a in l]
#x, y = zip(*[(document["timeStamp"],document["requestCount"])for document in cursor])
# print(x)
# print(y)

scaleValue = min(x)
xScaled = [(z - scaleValue)/100000.0 for z in x]

print(xScaled[-1])
print(max(xScaled))
print(max(y))
print(y[-1])
#print(y)

plt.plot(xScaled,y,'ro')
plt.axis([0, xScaled[-1], 0, y[-1]])
plt.show()