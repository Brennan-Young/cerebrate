from kafka import KafkaConsumer
import rethinkdb as r

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('flink-to-kafka',
                         group_id='test',
                         bootstrap_servers=['52.33.229.60:9092'])
r.connect( "35.163.48.63", 28015).repl()
r.table("cumulativeTest2").delete().run()
#r.db("test").table_create("cumulativeTest2").run()
for message in consumer:
    # cut out open and closing parentheses (artifact of scala's tuple)
    m = message.value[1:-1]
    # split on comma
    l = [x.strip() for x in m.split(',')]
    r.table("cumulativeTest2").insert([{"nodeID": int(l[0]), "timeStamp": long(l[1]), "requestCount": int(l[2])}]).run()