import java.util.Properties

import org.apache.flink.api.scala._
import org.apache.flink.streaming.util.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.scala.StreamExecutionEnvironment
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer09
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer09
import org.apache.flink.streaming.connectors.kafka.api.KafkaSink
import org.apache.flink.streaming.api.TimeCharacteristic
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.functions.AssignerWithPeriodicWatermarks
import org.apache.flink.streaming.api.watermark.Watermark

object getDemand {

// case class nodeEvent(nodeID: String, time:Long)

  def SimpleMovingAverage(input : Tuple3[String, Long, Int], windowSize: Int) : Tuple3[String, Long, Int] = {


return input
}

class TimestampExtractor extends AssignerWithPeriodicWatermarks[String] with Serializable {
  override def extractTimestamp(e: String, prevElementTimestamp: Long) = {
    e.split(" ")(1).toLong
  }
 override def getCurrentWatermark(): Watermark = {
      new Watermark(System.currentTimeMillis)
  }
}


  def main(args: Array[String]) {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)
    val properties = new Properties()
    properties.setProperty("bootstrap.servers", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092")
    properties.setProperty("zookeeper.connect", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:2181")
    properties.setProperty("group.id", "org.apache.flink")

    val stream = env
      .addSource(new FlinkKafkaConsumer09[String]("my-topic", new SimpleStringSchema(), properties))
      .assignTimestampsAndWatermarks(new TimestampExtractor)
/*
The next line is important for anyone trying to learn Scala and Flink at the same time.  TODO Explain why it's important
*/
    val parsedStream = stream.map(value => value.split("\\s+") match { case Array(x,y) => (x,y.toLong,1) })
//  TODO compute sliding window counts
    val requestCounts = parsedStream.keyBy(0).fold("0", 0L, 0)((s: (String, Long, Int), r: (String, Long, Int)) => { (r._1, s._2.max(r._2), s._3 + r._3) } )
 val packedStream = requestCounts.map(value => value.toString())
//   packedStream.print
    packedStream.addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "flink-to-kafka", new SimpleStringSchema()))

// Windowed Counting
//   val windowedCount = stream.map{(m: String) => (m.split(" ")(0)(1), 1) }
     val windowedCount = stream.map(value => value.split("\\s+") match { case Array(x,y) => (x,y.toLong,1)} )
				.keyBy(0)
				.timeWindow(Time.milliseconds(2000), Time.milliseconds(1000))
				.sum(2)
//				.map(value => (value._2)/2000)
     windowedCount.map(value => value.toString()).addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "demand-plots", new SimpleStringSchema()))

    env.execute("Flink Kafka Example")
  }
}

