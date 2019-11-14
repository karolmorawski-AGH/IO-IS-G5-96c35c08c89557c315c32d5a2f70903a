import networkx as nx
import matplotlib.pyplot as plt

class DrawGraph:
   G = nx.DiGraph()
   pos = nx.planar_layout(G)
   color_map=[]
   def drawGraph(self,matrix):

    array = matrix[0]
    array2 = matrix[1]

    '''
    array = [["",        "main.py", "graphgen.py", "pgraphdraw.py"],
             ["main.py",       "0",      "1",           "1"],
             ["graphgen.py",   "0",      "0",           "0"],
             ["pgraphdraw.py", "0",      "0",           "0"]]
    '''

   
    sum = [0] * len(array)

    for i in range(1, len(array)):
        for j in range(1, len(array)):
            sum[i] += int(array[i][j])

    for i in range(1, len(array)):
        for j in range(1, len(array)):
            if i != j and array[i][j] != "0":
                self.G.add_edge(array[i][0] + "\n" + str(sum[i]), array[0][j] + "\n" + str(sum[j]), length=array[i][j])

    '''
    array2 = [[],
              ["count_func", "filter_non_py", "get_imports", "get_graph",
               "show_info", "get_func_list", "list_func_calls", "get_graph_func"],
              ["drawGraph"]]
    '''

    for i in range(1, len(array)):
        if len(array2[i-1]) > 0:
            for j in range (0, len(array2[i-1])):
                self.G.add_edge(array2[i-1][j], array[i][0] + "\n" + str(sum[i]), length="")

   
    for node in self.G:
        if ".py" not in node:
            self.color_map.append('lightblue')
        else:
            self.color_map.append('lightgreen')

 
    nx.draw(self.G,self.pos,edge_color='black',width=0.5, node_size=1000,node_color=self.color_map, with_labels=True, font_size = 10)
    edge_labels=dict([((u,v,),d['length']) for u,v,d in self.G.edges(data=True)])
    nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, label_pos=0.4)
    plt.show()
