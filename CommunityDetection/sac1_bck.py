import sys, itertools, copy, math, csv
from igraph import *
import pandas as pd
import scipy.spatial
import operator
import sklearn, nltk

# provide alpha argument
if len(sys.argv)!=2:
	print("Please provide alpha value. For e.g. sac1.py <alpha>")
	sys.exit(1)

alpha = float(sys.argv[1])

# load data into a graph
g = Graph.Read_Edgelist('data/fb_caltech_small_edgelist.txt', directed=False)

# plot graph
#igraph.plot(g)

# getting the attribute list from csv file
global attrlist
attrlist = pd.read_csv('data/fb_caltech_small_attrlist.csv')
# getting the edges in the graph
global edges
edges = g.get_edgelist()

for edge in g.es():
	edge['weight'] = 1

for i in range(324):
	g.vs[i]['attr'] = attrlist.iloc[i]
	#print g.vs[i]['attr']

# getting the vertices in the graph
global vertices
vertices = set(list(itertools.chain(*edges)))

# Phase 1
# Initialize each node to a community
global communities
communities = { vertex:[vertex] for vertex in vertices }

# getting membership of the vertices
global membershiplist
membershiplist = [i for i in vertices]
#print(membershiplist)

def computer_similarity_matrix():
    similarity_matrix = [[sklearn.metrics.pairwise.cosine_similarity(attrlist.iloc[i], attrlist.iloc[j]) for j in vertices] for i in vertices]
    return similarity_matrix

def phase1(communities, x):

	similarity_matrix = computer_similarity_matrix()
	for k in range(x):
		print k
		print g.modularity(membershiplist)
		for i in vertices:
			#print("Cluster for "+str(i)+": Evaluating")
			max_gain = 0.0
			orig_QNewman = g.modularity(membershiplist)
			deltaQNewman = 0.0
			jMax = 0
			temp = membershiplist[i]
			for j in vertices:
				
				if (j == i or membershiplist[i] == membershiplist[j]):
					continue

				# update the membership
				membershiplist[i] = membershiplist[j]

				# get a new Q Newman value
				new_QNewman = g.modularity(membershiplist)
				
				# getting delta Q Newman value
				deltaQNewman = new_QNewman - orig_QNewman

				# getting delta Q Attribute value
				deltaQAttr = 0.0

				community = communities.get(membershiplist[j])

				for c in community:
					deltaQAttr += similarity_matrix[i][c]

				# length of community
				l = len(community)

				deltaQAttr = deltaQAttr / (l * l)
				deltaQAttr = deltaQAttr / len(set(membershiplist))
				
				# calculate the gain for current community
				deltaQ = alpha * deltaQNewman + (1 - alpha) * deltaQAttr 
				
				if deltaQ > max_gain:
					max_gain = deltaQ
					jMax = j

				membershiplist[i] = temp
			
			if max_gain > 0:
				communities.get(membershiplist[i]).remove(i)
				communities.get(membershiplist[jMax]).append(i)
				membershiplist[i] = membershiplist[jMax]

	communities = {k: v for k, v in communities.items() if v}
	return communities

def print_communities():
	count = 0
	for key in communities:
		if(communities[key]):
			#print(communities[key])
			count=count+1
	print(count)

def phase2(communities):
    mapping = [0 for i in range(0, 324)]
    vertex_id = 0
    for key in communities.keys():
	    community = communities[key]
	    for vertex in community:
	        mapping[vertex] = vertex_id
	    vertex_id += 1

    num_communities = len(communities)
    #print num_communities

    g.contract_vertices(mapping, combine_attrs=mean)

    for edge in g.es():
    	edge['weight'] = 1

	g.simplify(multiple=True, combine_edges=sum)
	
	edges = g.get_edgelist()
	vertices = set(list(itertools.chain(*edges)))
	membershiplist = [i for i in vertices]

	attrlist = pd.DataFrame()
    for vertex in g.vs:
        vector = vertex['attr']
        attrlist.append(vector)

    phase1(communities, 5)

    return communities

communities = phase1(communities, 15)

#print_communities()

communities = phase2(communities)

print_communities()