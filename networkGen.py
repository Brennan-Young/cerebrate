'''
This script establishes a random geometric graph, which models a randomly-distributed network of nodes in some two-dimensional space.  The graph is the primary input to the project, estasblishing the number of nodes and their locations.  
'''

import networkx as nx
from networkx.readwrite import json_graph
import json
import random
import matplotlib.pyplot as plt

def setNetworkParameters():
	'''
	Establishes parameters for the network.
	numNodes (int) : number of nodes (sensors, warehouses, etc.) in the network
	connectionRadius (float, 0-1) : maximum distance between connected vertices.  If two vertices are spaced by a distance smaller than connectionRadius, then there will be an edge between them. 
	'''
	numNodes = 200
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
	# print(G.edges())
	for e in G.edges():
		x1,y1 = pos[e[0]]
		x2,y2 = pos[e[1]]
		d = ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5
		G.edge[e[0]][e[1]]['weight'] = d 

	for node in G.nodes():
		# print(G.node[node]['pos'])
		G.node[node]['x'] = G.node[node]['pos'][0]
		G.node[node]['y'] = G.node[node]['pos'][1]
		del G.node[node]['pos']
		


	# json writing

	f=open('test.json','w')
	f.write('{\n"nodes": [\n')
	for i in range(len(G.nodes())-1):
		f.write('{\n\t"id": "n' + str(i) + '",\n')
		f.write('\t"label": "a' + str(i) + '",\n')
		f.write('\t"x": ' + str(G.node[i]['x']) + ',\n')
		f.write('\t"y": ' + str(G.node[i]['y']) + ',\n')
		f.write('\t"size": 1\n},\n')
	f.write('{\n\t"id": "n' + str(len(G.nodes())-1) + '",\n')
	f.write('\t"label": "a' + str(len(G.nodes())-1) + '",\n')
	f.write('\t"x": ' + str(G.node[len(G.nodes())-1]['x']) + ',\n')
	f.write('\t"y": ' + str(G.node[len(G.nodes())-1]['y']) + ',\n')
	f.write('\t"size": 1\n}\n')

	f.write('],\n"edges": [\n')
	for i in range(len(G.edges())-1):
		f.write('{\n\t"id": "e' + str(G.edges()[i][0]) + '_' + str(G.edges()[i][1]) + '",\n')
		f.write('\t"source": "n' + str(G.edges()[i][0]) + '",\n')
		f.write('\t"target": "n' + str(G.edges()[i][1]) + '"\n},\n')
	f.write('{\n\t"id": "e' + str(G.edges()[len(G.edges())-1][0]) + '_' + str(G.edges()[len(G.edges())-1][1]) + '",\n')
	f.write('\t"source": "n' + str(G.edges()[len(G.edges())-1][0]) + '",\n')
	f.write('\t"target": "n' + str(G.edges()[len(G.edges())-1][1]) + '"\n}\n')
	f.write(']}')

	f.close()


	# edgeFile = open('network.csv','w')	

	# edgeInfo = nx.get_edge_attributes(G,'weight')

	# for w in edgeInfo:
	# 	edgeFile.write(str(w[0]) + ',' + str(w[1]) + ',' + str(edgeInfo[w]) + '\n')
	# edgeFile.close()


	# supplyFile = open('supplies.csv','w')

	# supplyList = getSupplies(G, avgSupply, supplyDistribution, supplyVariance)
	# c = 0

	# for nodeSupply in supplyList:
	# 	supplyFile.write(str(c) + ',' + str(nodeSupply) + '\n')
	# 	c = c + 1
	# supplyFile.close()
	# print(G)
	# nx.write_gexf(G,"graph.gexf")
	# data = json_graph.node_link_data(G)
	# print(data)
	# with open('graphTest2.json','w') as out:
	# 	json.dump(data,out)
if __name__=="__main__":     
	main()
