from kafka import KafkaConsumer
import rethinkdb as r

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('demand-plots',
                         group_id='test',
                         bootstrap_servers=['52.33.229.60:9092'])
r.connect( "35.163.48.63", 28015).repl()
r.table("demandTest").delete().run()
# r.db("test").table_create("demandTest").run()

# batch writing 
batchSize = 1
batch = []

for message in consumer:
    # cut out open and closing parentheses (artifact of scala's tuple)
    m = message.value[1:-1]

    print(m)
    # split on comma
    l = [x.strip() for x in m.split(',')]

    doc = {"nodeID": int(l[0]), "timeStamp": long(l[1]), "requestCount": int(l[2])}
    batch.append(doc)
    if len(batch) >= batchSize:
    	print("a")
        r.table("demandTest").insert(batch).run()
        batch = []