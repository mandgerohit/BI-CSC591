__author__ = 'sandz'
import csv
import copy
from collections import defaultdict

from scipy import spatial
import igraph

# vertices = [i for i in range(323)]
g = igraph.Graph()
g = g.Read_Edgelist('data/fb_caltech_small_edgelist.txt')

columns = defaultdict(list)
with open('data/fb_caltech_small_attrlist.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            columns[k].append(int(v))
for key in columns:
    g.vs[key] = columns[key]

for edge in g.es():
    edge["weight"] = 1
# for v in g.vs():
# print v.attributes().values()


def compute_similarity_matrix(gr):
    similarity_matrix = []
    for vi in gr.vs():
        sim = []
        for vj in gr.vs():
            vi_a = vi.attributes().values()
            sim.append(1 - spatial.distance.cosine(vi.attributes().values(), vj.attributes().values()))
        similarity_matrix.append(sim)
    return similarity_matrix


vertices_attributes = []
counter = 0
va = []
for vertex_attributes in vertices_attributes:
    va.append(map(int, vertex_attributes))

i = 0

membership = range(len(g.vs()))
communities = {}

for i in range(324):
    communities[i] = [i]

def phase1():
    similarity_matrix = compute_similarity_matrix(g)

    for z in range(10):
        print z
        for i in range(324):
            original_mod = g.modularity(membership)
            location_i = i
            max_gain_i = 0
            for j in range(324):
                temp = copy.copy(membership)
                temp[i] = temp[j]
                gain_newman_mod = g.modularity(temp) - original_mod
                j_vers = communities.get(membership[j])
                sim_i_j = 0.0
                for j_ver in j_vers:
                    sim_i_j += similarity_matrix[i][j_ver]
                sim_i_j /= len(j_vers) ** 2
                c_sim_i_j = sim_i_j / len(set(membership))
                # print str(sim_i_j) + " " + str(gain_newman_mod) + "  " + str(c_sim_i_j)
                if gain_newman_mod + c_sim_i_j > max_gain_i:
                    max_gain_i = gain_newman_mod + c_sim_i_j
                    location_i = j
            old_location_i = membership[i]
            membership[i] = location_i
            j_vertices = communities.get(location_i)
            j_vertices.append(i)
            communities.get(old_location_i).remove(i)

    uniquemem = set(membership)
    print uniquemem
    print len(communities)

phase1()