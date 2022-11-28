import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

position = [(0,0),(0,1),(0,2)]
G = nx.DiGraph()
nodes_num = 3
nodes = [i for i in range(3)]
node_position = dict(zip(nodes,position))
G.add_nodes_from(nodes)

#初始化图的边
edge_num = 2
edges = [(0,1),(1,2)]
G.add_edges_from(edges)
nx.draw_networkx_nodes(G,pos=node_position)
nx.draw_networkx_edges(G,node_position)
plt.show()
