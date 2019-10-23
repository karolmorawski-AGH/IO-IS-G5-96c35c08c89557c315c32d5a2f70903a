import networkx as nx
import matplotlib.pyplot as plt

nodes = ['Main\n(2)','File1\n(2)','File2\n(2)']
lengths = [10,15,20]

G = nx.MultiDiGraph()
for i in range(0,len(nodes)):
    G.add_node(nodes[1])

G.add_edge(nodes[0], nodes[1], length=lengths[0])
G.add_edge(nodes[1], nodes[2], length=lengths[1])
G.add_edge(nodes[2], nodes[0], length=lengths[2])
G.add_edge(nodes[0], nodes[2], length=lengths[1])

pos = nx.spring_layout(G)
nx.draw(G,pos,edge_color='black',width=1, node_size=1000,node_color='lightgreen', with_labels=True)
edge_labels=dict([((u,v,),d['length']) for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
plt.show()