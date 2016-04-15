import sys, itertools, copy, math, csv
from igraph import *
import pandas as pd
import scipy.spatial
import operator
import sklearn, nltk
from sklearn.metrics.pairwise import cosine_similarity

# provide alpha argument
if len(sys.argv)!=2:
	print("Please provide alpha value. For e.g. sac1.py <alpha>")
	sys.exit(1)

alpha = float(sys.argv[1])

# load data into a graph
g = Graph.Read_Edgelist('data/fb_caltech_small_edgelist.txt', directed=False)

# getting the attribute list from csv file
global attrlist

with open("data/fb_caltech_small_attrlist.csv") as fileCSV:
	reader = csv.reader(fileCSV)
	attrlist = list(reader)[1:]

# getting the edges in the graph
edges = g.get_edgelist()

for edge in g.es():
	edge['weight'] = 1

for i in range(324):
	g.vs[i]['attr'] = attrlist[i]

# getting the vertices in the graph
vertices = g.vcount()

# Phase 1

# getting membership of the vertices
membershiplist = []
for i in range(vertices):
	membershiplist.append(i) 

# Initialize each node to a community
communities = list(Clustering(membershiplist))

# simplifying membershiplist to contact vertices
def simplify(membership):
	tempDict = {}
	memList = []
	count = 0 
	for i in membership:
		if i in tempDict.keys():
			memList.append(tempDict[i])
		else:
			memList.append(count);
			tempDict[i] = count
			count = count + 1
	return memList

#update the communities
def updateCommunities(community1, community2):
	result = []
	for i in community2:
		temp = []
		for j in i:
			temp = temp + community1[j]
		result.append(temp)
	return result

#computes updated similarity matrix
def update_similarity_matrix(community):
	similarity_matrix = [[0]*len(community)]*len(community)
	for i in range(len(community)):
		for j in range(len((community))):
			summation = 0
			for k in community[i]:
				for l in community[j]:
					summation = summation + copy_similarity_matrix[k][l]
			similarity_matrix[i][j] = summation
	return similarity_matrix

#computes similarity matrix
def compute_similarity_matrix():
	similarity_matrix = [[0]*len(attrlist)]*len(attrlist)
	for i in range(len(attrlist)):
		for j in range(len(attrlist)):
			similarity_matrix[i][j]=cosine_similarity(attrlist[i],attrlist[j])[0][0]
	return similarity_matrix

global similarity_matrix
similarity_matrix = compute_similarity_matrix()
global copy_similarity_matrix
copy_similarity_matrix = similarity_matrix

def phase1(membershiplist, x):
	vertices = len(set(membershiplist))
	for k in range(x):
		print k
		print g.modularity(membershiplist)
		for i in range(vertices):
			
			max_gain = 0.0
			orig_QNewman = g.modularity(membershiplist)
			deltaQNewman = 0.0
			jMax = -1
			temp = membershiplist[i]
			for j in range(vertices):
				
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

				# length of community
				l = 0
				for k in membershiplist:
					if(k == membershiplist[j]):
						l = l + 1

				for vertex, element in enumerate(membershiplist):
					if(membershiplist[j] == element):
						deltaQAttr = deltaQAttr + similarity_matrix[i][vertex]

				deltaQAttr = deltaQAttr / (l * l)
				deltaQAttr = deltaQAttr / len(set(membershiplist))
				
				# calculate the gain for current community
				deltaQ = alpha * deltaQNewman + (1 - alpha) * deltaQAttr 
				
				if deltaQ > max_gain:
					max_gain = deltaQ
					jMax = j

				membershiplist[i] = temp
			
			if max_gain > 0 and jMax != -1:
				membershiplist[i] = membershiplist[jMax]
	
	return membershiplist

# phase 2
def phase2(communities, membershiplist):

	# combining vertices in a single community
	membershiplist = simplify(membershiplist)

	g.contract_vertices(membershiplist)
	
	communities1 = list(Clustering(membershiplist))

	#updating communities to persist the original list
	communities = updateCommunities(communities, communities1)

	print communities

	similarity_matrix = update_similarity_matrix(communities)

	vertices = g.vcount() 

	#re initializing membershipList because some nodes might have collapsed
	membershiplist = []
	for i in range(vertices):
		membershiplist.append(i)
	
	membershiplist=[x for x in range(vertices)]

	#calling phase 1
	membershiplist = phase1(membershiplist, 15)

	membershiplist = simplify(membershiplist)
	communities1 = list(Clustering(membershiplist))
	communities = updateCommunities(communities, communities1)

	return communities

membershiplist = phase1(membershiplist, 15)

communities = phase2(communities, membershiplist)

out_file = open("communities.txt", "w+")
for com in communities:
	my = []
	for vertex in com:
		my.append(str(vertex))
	for i in range(len(my) - 1):
		out_file.write("%s," % str(my[i]))
	out_file.write("%s" % str(my[-1]))
	out_file.write("\n")

out_file.close()
