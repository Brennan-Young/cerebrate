// import java.util.Properties

import org.apache.flink.api.scala._
import scala.collection.mutable.ArrayBuffer
import org.apache.flink.graph.scala._
import org.apache.flink.graph.Edge
import org.apache.flink.graph.Vertex
import org.apache.flink.graph.scala.utils.Tuple3ToEdgeMap


object getNetworkInfo { 

def printdim(buffer: ArrayBuffer[Int]) = println(buffer mkString "x")

def readFile() : Graph[String, Long, Double] = {


    
	val env = ExecutionEnvironment.getExecutionEnvironment


    val graph = Graph.fromCsvReader[String, Long, Double](
		pathVertices = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/supplies.csv",
		pathEdges = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/network.csv",
		env = env)


	return graph

}








}