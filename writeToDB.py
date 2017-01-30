from kafka import KafkaConsumer
import rethinkdb as r

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('flink-to-kafka',
                         group_id='test',
                         bootstrap_servers=['52.33.229.60:9092'])
r.connect( "35.163.48.63", 28015).repl()
r.db("test").table_create("kafka").run()
for message in consumer:
	r.table("kafka").insert([{"name":str(message.value)}]).run()