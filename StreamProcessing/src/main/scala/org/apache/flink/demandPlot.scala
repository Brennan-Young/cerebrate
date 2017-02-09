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

  // Useful function to convert a string to an int by value but not by reference.  Similar to python's sort(x) vs sorted(x).  
  def getInt(x:  String) : Int = {return x.toInt}

  class TimestampExtractor extends AssignerWithPeriodicWatermarks[String] with Serializable {
    override def extractTimestamp(e: String, prevElementTimestamp: Long) = {
      e.split(" ")(1).toLong
    }
    override def getCurrentWatermark(): Watermark = {
      new Watermark(System.currentTimeMillis)
    }
  }


  def main(args: Array[String]) {


    // val graph = getNetworkInfo.readFileAsGraph
    // val v = graph.getVertices
    // // v(1).print
    // val v2 = v.filter(vertex => {vertex.getId == "1" }  )
    // v2.print

    val (vertexArray, edgeArray) = getNetworkInfo.readFileAsList



    // establish streaming environment
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)

    // get streamed data from Kafka
    val properties = new Properties()
    properties.setProperty("bootstrap.servers", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092")
    properties.setProperty("zookeeper.connect", "ec2-52-33-229-60.us-west-2.compute.amazonaws.com:2181")
    properties.setProperty("group.id", "org.apache.flink")

    val stream = env
        .addSource(new FlinkKafkaConsumer09[String]("my-topic", new SimpleStringSchema(), properties))
        .assignTimestampsAndWatermarks(new TimestampExtractor)

    val pStream = stream.map(value => value.split("\\s+") match { case Array(x,y) => (x,y.toLong,0) })
    val keyStream = pStream.keyBy(0)
        /*
        This next block is pretty good and merits some explanation.  mapWithState takes the keyed stream data and assigns a state to model the supply at a node.  If no state has been assigned (initial case), a supply of 500 will be assigned.  If the supply is greater than 400, the supply will be decremented when a new request is seen.  If the supply dips below 400, a flag is set.  
        */
        .mapWithState{
          (value , supply: Option[Int]) => 
            supply match{
              case Some(counter) if 0 until 400 contains counter =>
                (value match{ 
                  case r: (String,Long,Int) => 
                    (r._1,r._2,1) }, Some(counter-1))
              case Some(counter) =>
                (value, Some(counter - 1))
              case None => 
                (value, Some(vertexArray(getInt(value._1))._2))
            }
          } 
        .print


    /*
    The next line is important for anyone trying to learn Scala and Flink at the same time.  TODO Explain why it's important
    */
    // split input string on spaces, turn into tuple with the number 1 appended
    val parsedStream = stream.map(value => value.split("\\s+") match{ 
      case Array(x,y) => (x,y.toLong,1) 
    })
    // key on node ID and record running counts of requests
    val requestCounts = parsedStream.keyBy(0)
        .fold("0", 0L, 0)(
          (s: (String, Long, Int), r: (String, Long, Int)) => {
            (r._1, s._2.max(r._2), s._3 + r._3) 
          }
        )
    // pack back into string for Kafka
    val packedStream = requestCounts.map(value => value.toString())
    // packedStream.print
    // Kafka sink
    packedStream.addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "flink-to-kafka", new SimpleStringSchema()))

    // Windowed Counting
    /* 
    split input string on spaces, turn into tuple with the number 1 appended.  Key on node ID.  Count all requests in a key that happened in the last 2 seconds, with the window advancing by 1 second.
    */
    // val windowedCount = stream.map{(m: String) => (m.split(" ")(0)(1), 1) }
    val windowedCount = stream.map(value => value.split("\\s+") match { case Array(x,y) => (x,y.toLong,1)} )
        .keyBy(0)
        .timeWindow(Time.milliseconds(2000), Time.milliseconds(1000))
        .sum(2)
    // pack into string for Kafka and add a sink
    windowedCount.map(value => value.toString()).addSink(new FlinkKafkaProducer09[String]("ec2-52-33-229-60.us-west-2.compute.amazonaws.com:9092", "demand-plots", new SimpleStringSchema()))

    env.execute("Flink Kafka Example")
  }
}

