
import networkx as nx
import matplotlib.pyplot as plt

class DrawGraph:

    pos = self.nx.spring_layout(G)
    def drawGraph(x):   
        for i in range(0, len(x)):
           G.add_edge(x[i][0], x[i][1], length=x[i][2])
        nx.draw(G,pos,edge_color='black',width=1, node_size=1000,node_color='lightgreen', with_labels=True)
        edge_labels=dict([((u,v,),d['length']) for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
        plt.show()

