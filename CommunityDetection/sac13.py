from igraph import *
import csv
import pandas as pd
import scipy.spatial

# f = open('fb_caltech_small_attrlist.csv', 'rb')
# f.next()
# contents = csv.reader(f, delimiter=',')
#
# print contents

g = Graph()
attributes = pd.DataFrame()
communities = {vertex: [vertex] for vertex in range(0, 324)}


def main():
    process_data()
    communities = phase1()
    phase2(communities)
    print len(communities)


def process_data():
    edges = []
    f_edgelist = open('fb_caltech_small_edgelist.txt', 'rb')

    for edge in open('fb_caltech_small_edgelist.txt', 'rb'):
        edges.append(tuple(map(int, edge.rstrip().split(' '))))

    global g
    g = Graph.Read_Edgelist(f_edgelist, directed=False)
    global attributes
    attributes = pd.read_csv('fb_caltech_small_attrlist.csv')

    for i in range(0, 324):
        g.vs[i]['attr'] = attributes.iloc[i]

    print 'Length of attributes = ' + str(len(attributes))


def phase1():
    # Phase 1
    alpha = 1.0

    num_vertices = len(attributes)
    vertices = [i for i in range(0, num_vertices)]
    membership_nodes = [i for i in vertices]

    similarity_matrix = []
    for i in range(0, num_vertices):
        sim = []
        for j in range(0, num_vertices):
            sim.append(1 - scipy.spatial.distance.cosine(attributes.iloc[i], attributes.iloc[j]))
        similarity_matrix.append(sim)

    for k in range(0, 15):
        print "Iteration " + " " + str(k)
        for i in vertices:
            # print("Cluster for "+str(vertex1)+": Evaluating")
            modularity_gain = {}
            for j in vertices:
                deltaq_attr = 0.0
                if j == i:
                    continue
                new_membership_nodes = list(membership_nodes)
                new_membership_nodes[i] = new_membership_nodes[j]
                deltaq_newman = g.modularity(new_membership_nodes) - g.modularity(membership_nodes)

                #similarity
                # get community to which j belongs
                # community = communities[membership_nodes[j]]
                # # calculate sim of vertex1 with all vertices in community of vertex2 and sum
                # for vertex in community:
                #     deltaq_attr += similarity_matrix[i][vertex]
                #
                # community_size = len(community)
                #
                # deltaQ_attr = deltaQ_attr / community_size / community_size
                modularity_gain[j] = alpha * deltaq_newman + (1 - alpha) * deltaq_attr

            if len(modularity_gain) > 0:
                max_j = max(modularity_gain.items(), key=operator.itemgetter(1))[0]
                if modularity_gain[max_j] > 0:
                    key_vertex2_max = membership_nodes[max_j]
                    key_vertex1 = membership_nodes[i]
                    membership_nodes[i] = membership_nodes[max_j]
                    global communities
                    communities[key_vertex1] = list(set(communities[key_vertex1]) - set([i]))
                    communities[key_vertex2_max] += [i]

    communities = {k: v for k, v in communities.items() if v}
    return communities


def phase2(communities):
    mapping = [0 for i in range(0, 324)]
    vertex_id = 0
    for key in communities.keys():
        community = communities[key]
        for vertex in community:
            mapping[vertex] = vertex_id
        vertex_id += 1

    num_communities = len(communities)
    g.contract_vertices(mapping, combine_attrs=mean)

    for i in range(0, num_communities):
        g.es['weight'] = 1

    g.simplify(multiple=True, combine_edges=sum)

    # for edge in g.es:
    #     print edge['weight']

    global attributes
    attributes = pd.DataFrame()
    for vertex in g.vs:
        vector = vertex['attr']
        attributes.append(vector)

    phase1()

main()