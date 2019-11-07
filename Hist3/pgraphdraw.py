import networkx as nx
import matplotlib.pyplot as plt

def drawGraph(array):

    array = [["",        "main.py", "graphgen.py", "pgraphdraw.py"],
             ["main.py",       "0",      "4",           "1"],
             ["graphgen.py",   "0",      "0",           "0"],
             ["pgraphdraw.py", "0",      "0",           "0"]]

    G = nx.DiGraph()
    sum = [0] * len(array)

    for i in range(1, len(array)):
        for j in range(1, len(array)):
            sum[i] += int(array[i][j])

    for i in range(1, len(array)):
        for j in range(1, len(array)):
            if i != j and array[i][j] != "0":
                G.add_edge(array[i][0] + "\n" + str(sum[i]), array[0][j] + "\n" + str(sum[j]), length=array[i][j])

    array2 = [[],
              ["count_func", "filter_non_py", "get_imports", "get_graph",
               "show_info", "get_func_list", "list_func_calls", "get_graph_func"],
              ["drawGraph"]]

    for i in range(1, len(array)):
        if len(array2[i-1]) > 0:
            for j in range (0, len(array2[i-1])):
                G.add_edge(array2[i-1][j], array[i][0] + "\n" + str(sum[i]), length="")

    color_map=[]
    for node in G:
        if ".py" not in node:
            color_map.append('lightblue')
        else:
            color_map.append('lightgreen')

    pos = nx.planar_layout(G)
    nx.draw(G,pos,edge_color='black',width=0.5, node_size=1000,node_color=color_map, with_labels=True, font_size = 10)
    edge_labels=dict([((u,v,),d['length']) for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.4)
    plt.show()






