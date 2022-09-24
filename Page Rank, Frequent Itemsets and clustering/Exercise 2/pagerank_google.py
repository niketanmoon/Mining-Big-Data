import numpy as np

# Can have a read about coo_matrix vs csc_matrix at this link https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html
from scipy.sparse import coo_matrix

from collections import defaultdict
import sys
import time

start_time = time.time()

print(f"Program started at {time.ctime(start_time)}")

incoming_links_dict = defaultdict(int)
outgoing_links_dict = defaultdict(int)

from_node_id_list = list()
to_node_id_list = list()

filename = sys.argv[1]
with open(filename, "r", encoding="utf-8") as f:
    # going through each line in file
    for idx, line in enumerate(f):
        
        """
        If the line starts with # that means we have to skip it 
        This is because the file has some chunks telling the description about number of nodes and edges
        It also tells us about the two columns
        first- fromNodeId
        second- toNodeId
        """
        if line[0] == "#":
            continue
        
        from_node_id, to_node_id =  map(int, line.split())
        
        # There is a link from from_node_id to to_node_id
        # from_node_id --> to_node_id
        # i.e. increase the outgoing link for from_node_id and increase the incoming link for to_node_id
        outgoing_links_dict[from_node_id] += 1
        incoming_links_dict[to_node_id] += 1
        
        # and then add the nodes to the respective list 
        from_node_id_list.append(from_node_id)
        to_node_id_list.append(to_node_id)

# finding nodes that have no incoming and outgoing node
# this will happen when there is no node inside the incoming or outgoing dicts for that particular node
for idx in range(500):
    if incoming_links_dict[idx] == 0 and outgoing_links_dict[idx] == 0:
        print(idx, end="\t")
print("\n")

# Store all the original stuff as it is 
# Make a list of all nodes
original_nodes_present = sorted(list(set(from_node_id_list) | set(to_node_id_list)))

# Make a dict of the nodeId and index it was in
original_nodes_present_dict = dict([(val, idx) for idx, val in enumerate(original_nodes_present)])

original_from_node_list = [original_nodes_present_dict[node_id] for node_id in from_node_id_list]
original_to_node_list = [original_nodes_present_dict[node_id] for node_id in to_node_id_list]

data = [1./ outgoing_links_dict[node_id] for node_id in from_node_id_list]

# Making a probability transition matrix with rows indices (original_to_node_id_list) and column indices (original_from_node_id_list) 

M = coo_matrix((data, (original_to_node_list, original_from_node_list)))

# Now copying the algorithm from solution 1 implemented in pagerank.py
# Number of nodes
beta= 0.8
ep = 1./(10**10)
nodes = M.shape[0]
v = np.zeros((nodes, 1)) + 1./nodes

E = np.ones((nodes, 1))

for _ in range(1, 250):
    new_v = beta*M*v + (1-beta)*E/nodes
    
    if np.sum(np.abs(new_v - v)) < ep:
        break
    v = new_v

v = v/np.sum(v)

# dict of key as nodes and value as pagerank
pagerank_nodes_dict = {}

with open("output_file.txt", "w") as f:
    for idx, val in enumerate(v):
        pagerank_nodes_dict[idx] = val[0]
        f.write(f"{idx} {val[0]}")
        f.write("\n")

# getting the top 10 nodes of highest pagerank
top_10 = sorted(pagerank_nodes_dict, key=pagerank_nodes_dict.get, reverse=True)[:10]

# wrtiting the top ten nodes with their values
with open("top_10_output_file.txt", "w") as f:
    f.write(f"{top_10}")
    f.write("\n")
    for node in top_10:
        f.write(f"{node} {pagerank_nodes_dict[node]}")
        f.write("\n")

end_time = time.time()
print(f"Program ended at {time.ctime(end_time)}")
print(f"Execution time:     {end_time - start_time} seconds")