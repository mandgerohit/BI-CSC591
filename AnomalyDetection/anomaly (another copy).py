import sys, collections, nltk, random, csv, math, copy
import sklearn.naive_bayes
import sklearn.linear_model
import scipy
import numpy as np
from igraph import *
from collections import defaultdict
from operator import add
import matplotlib.pyplot as plt
import md5
import binascii

def createGraph(file):
	f = open(file, 'rb')
	lines = f.readlines()
	vertex_count = int(lines[0].split()[0])
	edge_count = int(lines[0].split()[1])
	g = Graph(vertex_count, directed = True)
	for i in range(len(lines)):
		if i == 0:
			continue;
		v1 = int(lines[i].split()[0])
		v2 = int(lines[i].split()[1])
		g.add_edges([(v1, v2)])
	return g

def getFeatures(g):
	pageranks = g.pagerank()
	g.vs["quality"] = pageranks
	g.es["weight"] = [1]*len(g.es)
	outdegrees = g.outdegree()
	features = []
	for vertex in g.vs:
		feature = ['v'+str(vertex.index), vertex["quality"]]
		features.append(feature)
	for edge in g.es:
		quality = g.vs["quality"][edge.tuple[0]] / float(outdegrees[edge.tuple[0]])
		feature = ['e'+str(edge.tuple[0])+'-'+str(edge.tuple[1]), quality]
		features.append(feature)
	return features


def createSimHash(features):
	sim_hash = [0]*32
	graph_sim_hash = []
	for feature in features:
		m = md5.new(feature[0])
		digest = bin(int(binascii.hexlify(m.digest()),16))
		hashlist = digest[-32:]
		sim_hash_feature = []
		for point in hashlist:
			if point == '0':
				sim_hash_feature.append(feature[1])
			else:
				sim_hash_feature.append(-1*feature[1])
		sim_hash = map(add, sim_hash, sim_hash_feature)
	for element in sim_hash:
		if(element < 0):
			graph_sim_hash.append(0)
		else:
			graph_sim_hash.append(1)
	return graph_sim_hash

def findSimilarity(g1, g2):
	features1 = getFeatures(g1)
	simhash1 = createSimHash(features1)
	features2 = getFeatures(g2)
	simhash2 = createSimHash(features2)
	similarity = 1-(scipy.spatial.distance.hamming(simhash1, simhash2)/32)
	return similarity

def main(argv):
	similarities = []
	diff_similarities = []
	for i in range(int(argv[1])):
		filename = 'datasets/'+argv[0]+'/'+str(i)+'_'+argv[0]+'.txt'
		g1 = createGraph(filename)
		if(i > 0):
			similarities.append(findSimilarity(g1, g2))
		g2 = g1

	for i in range(len(similarities)):
		if(i == 0):
			continue
		diff_similarities.append(abs(similarities[i]-similarities[i-1]))

	mean = sum(diff_similarities)/len(diff_similarities)
	median = median(similarities)
	lower_bound = median - (3*mean)
	
	anomaly_index = []
	anomaly_value = []
	for i in range(len(similarities)):
		if similarities[i] < lower_bound:
			anomaly_value.append(similarities[i])
			anomaly_index.append(i)

	plt.plot(range(len(similarities)),similarities, 'g-', label='Similarities')

	plt.plot(anomaly_index, anomaly_value, 'bD', label="Threshold Exceed")
	
	anomaly_point_value = []
	anomaly_point_index = []
	for i in range(len(anomaly_value)):
		if((anomaly_index[i]+1) in anomaly_index):
			anomaly_point_index.append(anomaly_index[i])
			anomaly_point_value.append(anomaly_value[i])
	plt.plot(anomaly_point_index, anomaly_point_value, 'ro', label="Anomalous Graph")
	filename = argv[0] + '_time_series.txt'
	with open(filename, 'w') as f:
		for i in range(len(similarities)):
			f.write(str(i))
			f.write(",")
			f.write(str(similarities[i]))
			f.write('\n')
	filename = argv[0] + '_plot.pdf'
	plt.legend()
	plt.savefig(filename)
	plt.show()


if __name__ == "__main__":
   main(sys.argv[1:])