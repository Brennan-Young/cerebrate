import java.util.Properties

import org.apache.flink.api.scala._
import org.apache.flink.streaming.util.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer09
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer09
import org.apache.flink.streaming.connectors.kafka.api.KafkaSink



object Main {
  def main(args: Array[String]) {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
//    env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
    val properties = new Properties()
    println("hello")
    properties.setProperty("bootstrap.servers", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092")
    properties.setProperty("zookeeper.connect", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:2181")
    properties.setProperty("group.id", "org.apache.flink")
    println("hello")
    val stream = env
      .addSource(new FlinkKafkaConsumer09[String]("my-topic", new SimpleStringSchema(), properties))
    //val splitStream = stream.map(value => (value.split("\\s+")))
    //val (a,b,c) = (splitStream(0), splitStream(1), splitStream(2))

//    val timestampedStream = stream.assignTimestamps{new timestampExtractor()}
  //  val x = timestampedStream.flatMap(value => value.split("\\s+")).map(value => (value,1)).print
    //splitStream collect { case Array(x: String, y: String, _*) => (x,y) }
    //val z = splitStream.print
  //  val x = splitStream match {case Array(f1,f2,f3) => (f1,f2,f3)}
    //val y = x.print

//    val splitStream = stream.map(value => value.split("\\s+")).map{case Array(f1: String, f2: String) => (f1,f2,1)}.print
//  val keyValuePair = splitStream.keyBy(0)
//    val countPair = keyValuePair.sum(1).print
/*    val wordsStream = stream.flatMap(value => value.split("\\s+")).map(value => (value,1))

    val keyValuePair = wordsStream.keyBy(0)

    val countPair = keyValuePair.sum(1).print
    val timestamp: Long = System.currentTimeMillis / 1000
    val y = (countPair._2, timestamp)
    val z = y.print
*/
//    val x =  countPair.addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "flink-to-kafka", new SimpleStringSchema()))

   /* stream.addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "flink-to-rethinkdb", new SimpleStringSchema()))
*/
/*    val x =  stream.addSink(new KafkaSink("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "flink-output", new MySimpleStringSchema))
  */  println("hello")
    env.execute("Flink Kafka Example")
    println("hello")
  }
}
