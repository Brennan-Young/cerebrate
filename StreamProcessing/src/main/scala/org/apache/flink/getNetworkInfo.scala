// import java.util.Properties

import org.apache.flink.api.scala._
import scala.collection.mutable.ArrayBuffer
import org.apache.flink.graph.scala._
import org.apache.flink.graph.Edge
import org.apache.flink.graph.Vertex
import org.apache.flink.graph.scala.utils.Tuple3ToEdgeMap
import scala.io.Source


object getNetworkInfo { 

	def readFileAsGraph() : Graph[String, Long, Double] = {

	/*
	Reads information about the network from Hadoop Distributed File System.  Places this network information into a graph and returns the graph data object. The network information comes in two csv files:

	supplies.csv: a comma separated values sequence, where the first field is the node (sensor) ID and the second field is the initial supply at that sensor.

	network.csv: a comma separated values sequence, where the first field is the ID of the source node, the second field is the ID of the target node, and the third field is the distance between these (the edge weight)

	*/
	    
		val env = ExecutionEnvironment.getExecutionEnvironment

		/* 
		String: vertex ID type
		Long: vertex attribute type
		Double: edge attribute type
		edge source/target types are implicitly string as the vertex ID types are strings
		*/
	    val graph = Graph.fromCsvReader[String, Long, Double](
			pathVertices = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/supplies.csv",
			pathEdges = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/network.csv",
			env = env)


		return graph

	}

	def readFileAsList() : (Array[(String, Int)], Array[(String,String,Double)]) = {
		// val vertexArray = Array[(String, Long)]()
		// val vertexFile = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/supplies.csv"
		// for (line <- Source.fromFile(vertexFile).getLines()) {
  // 		// vertexArray :+ line.map(string => string.split(",") match  {case Array(x,y) => (x,y.toLong)})
  // 		vertexArray :+ line.split(",") match  {case Array(x,y) => (x,y.toLong)}
		// }

		// val edgeArray = Array[(String, String, Double)]()
		// val edgeFile = "hdfs://ec2-52-33-88-184.us-west-2.compute.amazonaws.com:9000/test/network.csv"
		// for (line <- Source.fromFile(edgeFile).getLines()) {
  // 		// edgeArray :+ line.map(string => string.split(",") match  {case Array(x,y,z) => (x,y,z.toDouble)})
  // 		edgeArray :+ line.split(",") match  {case Array(x,y,z) => (x,y,z.toDouble)}
		// }

		val vertexFile = "./src/main/resources/supplies.csv"
		val vertexArray = Source.fromFile(vertexFile)
				.getLines()
				.map(string => 
					string.split(",") match {
						case Array(x,y) => (x,y.toInt)
					}
				)
				.toArray


		val edgeFile = "./src/main/resources/network.csv"
		val edgeArray = Source.fromFile(edgeFile)
				.getLines()
				.map(string => 
					string.split(",") match {
						case Array(x,y,z) => (x,y,z.toDouble)
					}
				)
				.toArray


		// println(vertexArray.deep.mkString("\n"))
		// println(edgeArray.deep.mkString("\n"))

		return (vertexArray, edgeArray)

	}
}