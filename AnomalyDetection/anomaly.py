import matplotlib.pyplot as plt
from os import listdir
import scipy.spatial
from statistics import median
import networkx as nx
import hashlib
import random
import sys

def createGraph(file):
	f = open(file, 'rb')
	lines = f.readlines()
	vertex_count = int(lines[0].split()[0])
	edge_count = int(lines[0].split()[1])
	g = nx.DiGraph()

	for i in range(len(lines)):
		if i == 0:
			continue;
		v1 = int(lines[i].split()[0])
		v2 = int(lines[i].split()[1])
		g.add_edge(v1, v2)
	return g

def getFeatures(g):
	page_rank = nx.pagerank(g)
	feature_set = [ (str(ti),wi) for ti,wi in page_rank.items() ]

    #Calculating the weights of edges.
	for edge in g.edges():
		ti = str(edge[0]) + ' ' + str(edge[1])
		out_degree = g.out_degree(edge[0])       
		wi = page_rank[ edge[0] ] /out_degree 
		feature_set.append( (ti,wi) )
	return feature_set

def createSimHash(features):
	vector = [0]*32
	for ti, wi in features:
	    #Create a hash on ti
	    hex_dig = hashlib.md5( ti.encode('utf-8') ).hexdigest()
	    bin_repr = bin( int( hex_dig, 16) )[2:].zfill(32)       

	    #+wi for each 1 in hash, -wi for each 0
	    for i in range(32):
	        if bin_repr[i] == '1':
	            vector[i] = vector[i] + wi  
	        else: 
	            vector[i] = vector[i] - wi
    #Replcaing each positive number by 1 and each negative number by 0 in the simHash
	for i in range(32):
	    if vector[i] > 0: vector[i] = 1  
	    else: vector[i] = 0
	return(vector)

def calculateSimilarity(simhash1, simhash2):
	b = len(simhash1)
	similarity = 1-(scipy.spatial.distance.hamming(simhash1, simhash2)/b)
	return similarity

def calculateThreshold(similarity_list):
    med = median(similarity_list)
    n = len(similarity_list)
    if n < 2: return(med)
    diff_similarity_list = []
    
    #Calculating MR which is moving average of similarities
    for i in range(len(similarity_list)):
        diff_similarity_list.append(abs(similarity_list[i] - similarity_list[i-1]))

    mean = sum(diff_similarity_list)/(n-1)
    lower_bound = med - (3*mean)
    #Return a dictionary with lower threshold and median value
    return( {"lower": lower_bound, "median": med, "mean" : mean} )

def plotResults(similarities, threshold, filename):
	mr_multiplier = 3
	plt.plot(range( len(similarities) ), similarities, 'r', color = 'blue' )
	plt.title('Threshold: (Median - ' + str(mr_multiplier) + ' * MR)' )
	plt.xlabel('Index')
	plt.ylabel('Similarity')
	plt.grid(True)   
	#Draw horizontal line for threshold.
	line1, = plt.plot([0, len(similarities)], [threshold["lower"], threshold["lower"]], 'k--', lw=1, alpha=0.75)
	plt.legend([line1], ['Threshold'])
	plt.savefig(filename)

def writeOutput(similarities, filename):

	with open(filename, 'w') as f:
		for i in range(len(similarities)):
			f.write(str(i))
			f.write(",")
			f.write(str(similarities[i]))
			f.write('\n')
	f.close()

def main(argv):
	similarities = []
	simhash_list = []
	data_directory = 'datasets/'+ argv[0] + '/'
	#Sort the file list based on integer before underscore
	file_list = sorted( listdir(data_directory), key=lambda item: (int(item.partition('_')[0])) )
	for filename in file_list:
		filename = 'datasets/'+argv[0]+'/'+filename
		print(filename)
		g = createGraph(filename)
		features = getFeatures(g)
		g.clear()

        #Calculate Simhash signatures based on feature set
		sim_hash_vector = createSimHash(features)
		simhash_list.append(sim_hash_vector)
    
   	#get Similarities
	for x,y in zip( simhash_list, simhash_list[1:] ):
		similarity = calculateSimilarity(x,y)
		similarities.append(similarity)
	
	print(similarities)
	multiplier = 3
	out_put_file = argv[0] + '_time_series'

	threshold = calculateThreshold(similarities)

	#Plot the results
	plotResults(similarities, threshold, out_put_file+".png")

	#write output
	writeOutput(similarities, out_put_file+".txt")

if __name__ == "__main__":
   main(sys.argv[1:])