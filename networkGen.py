'''
This script establishes a random geometric graph, which models a randomly-distributed network of nodes in some two-dimensional space.  The graph is the primary input to the project, estasblishing the number of nodes and their locations.  
'''

import networkx as nx
import random
import matplotlib.pyplot as plt

def setNetworkParameters():
	'''
	Establishes parameters for the network.
	numNodes (int) : number of nodes (sensors, warehouses, etc.) in the network
	connectionRadius (float, 0-1) : maximum distance between connected vertices.  If two vertices are spaced by a distance smaller than connectionRadius, then there will be an edge between them. 
	'''
	numNodes = 2000
	connectionRadius = 0.1
	avgSupply =  500
	supplyDistribution = 'gaussian'
	supplyVariance = 50 
	return numNodes, connectionRadius, avgSupply, supplyDistribution, supplyVariance

def getSupplies(graph, averageSupply, supplyDistribution, supplyVariance):
	'''
	Assigns an initial supply to every node in the network.
	'''
	supplyList = []
	if supplyDistribution == 'gaussian':
		for node in graph.nodes():
			supply = int(round(random.gauss(averageSupply, supplyVariance)))
			supplyList.append(supply)
	# n, bins, patches = plt.hist(supplyList, 20, normed=1, facecolor='green', alpha=0.75)
	# plt.show()
	return supplyList


def main():
	'''
	Builds network and writes all vertex positions and edge information to a text file for use with realTimeGen.py and Flink job.  
	'''
	numNodes, connectionRadius, avgSupply, supplyDistribution, supplyVariance = setNetworkParameters()
	G = nx.random_geometric_graph(numNodes, connectionRadius)

	pos = nx.get_node_attributes(G,'pos')
	print(G.edges())
	for e in G.edges():
		x1,y1 = pos[e[0]]
		x2,y2 = pos[e[1]]
		d = ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5
		G.edge[e[0]][e[1]]['weight'] = d 
	getSupplies(G, avgSupply, supplyDistribution, supplyVariance)

	
	nx.write_multiline_adjlist(G,'test.out')



if __name__=="__main__":     
	main()
