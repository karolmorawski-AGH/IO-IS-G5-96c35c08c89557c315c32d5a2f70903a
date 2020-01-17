import networkx as nx
import matplotlib.pyplot as plt
import graph_generator as gg
import git


# This module contains DrawGraph class with methods corresponding to drawing specific type of graph
# Uses graph_generator module methods for getting graph representations and then interprets them
# accordingly
def getVer():
    try:
        repo = git.Repo('../../')
        sha = repo.head.object.hexsha
    except:
        sha = 'unknown'
    return sha

class DrawGraph:
    # Default dirpath and gg class
    dirpath = "./"

    # Constructor
    def __init__(self, dirpath):
        self.dirpath = dirpath

    # Draws file relationship graph
    def draw_file_graph(self):
        file_graph_gen = gg.FileGraphGenerator(self.dirpath)
        x = file_graph_gen.get_graph()
        plt.figure(figsize=(12, 12))

        G = nx.DiGraph()
        for i in range(0, len(x)):
            G.add_edge(x[i][0], x[i][1], length=x[i][2])

        plt.title("Version: " + getVer())
        pos = nx.spring_layout(G)
        nx.draw(G, pos, edge_color='black', width=1, node_size=1000, node_color='lightgreen', with_labels=True)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
        plt.show()

    # Draws method relationship graph
    def draw_method_graph(self):

        method_graph = gg.MethodGraphGenerator("./")
        graph = method_graph.get_graph()

        # Get func list
        func = []
        i = 0
        while i < len(graph):
            if i != 0:
                func.append(graph[i][0])
            i += 1

        # Set node values for func list
        nvalues = []
        i = 1
        j = 1
        while i < len(graph):
            summ = 0
            j = 1
            while j < len(graph[i]):
                summ += graph[i][j]
                j += 1
            func[i-1] += '\n' + str(summ)
            i += 1


        # Set edge values for func list

        #method_graph.print_representation(graph)
        plt.figure(figsize=(12, 12))
        G = nx.DiGraph()
        for i in range(0, len(func)):
            G.add_node(func[i])


        for i in range(0, len(func)):
            summ = 0
            for j in range(0, len(graph[i+1])-1):
                if graph[i+1][j+1] != 0:
                    G.add_edge(func[i], func[j], length=graph[i+1][j+1])

        plt.title("Version: " + getVer())
        pos = nx.circular_layout(G)
        nx.draw(G, pos, edge_color='black', width=1, node_size=750, node_color='lightblue', with_labels=True)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
        print('Graph saved into /graphs directory')
        #plt.savefig('../../graphs/method_r_' + getVer(), dpi=500)
        plt.show()

    # Draws module relationship graph
    def draw_module_graph(self):

        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)

        array = module_graph_gen.get_graph()[0]
        array2 = module_graph_gen.get_graph()[1]

        plt.figure(figsize=(12, 12))
        graphx = nx.DiGraph()
        sum = [0] * len(array)

        for i in range(1, len(array)):
            for j in range(1, len(array)):
                sum[i] += int(array[i][j])

        for i in range(1, len(array)):
            for j in range(1, len(array)):
                if i != j and array[i][j] != "0":
                    graphx.add_edge(array[i][0] + "\n" + str(sum[i]), array[0][j] + "\n" + str(sum[j]),
                                    length=array[i][j])

        for i in range(1, len(array)):
            if len(array2[i - 1]) > 0:
                for j in range(0, len(array2[i - 1])):
                    graphx.add_edge(array2[i - 1][j], array[i][0] + "\n" + str(sum[i]), length="")

        color_map = []
        for node in graphx:
            if ".py" not in node:
                color_map.append('lightblue')
            else:
                color_map.append('lightgreen')

        plt.title("Version: " + getVer())
        pos = nx.spring_layout(graphx)
        nx.draw(graphx, pos, edge_color='black', width=0.5, node_size=1000, node_color=color_map, with_labels=True,
                font_size=10)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in graphx.edges(data=True)])
        nx.draw_networkx_edge_labels(graphx, pos, edge_labels=edge_labels, label_pos=0.4)
        plt.show()

    # File + Module graph
    # TODO
    def draw_file_module_graph(self):
        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)
        file_graph_gen = gg.FileGraphGenerator(self.dirpath)

        x = file_graph_gen.get_graph()
        print(x)
        print(len(x))
        array = module_graph_gen.get_graph()[0]
        array2 = module_graph_gen.get_graph()[1]

        plt.figure(figsize=(12, 12))
        graphx = nx.MultiDiGraph()

        # FOR module graph
        sum = [0] * len(array)

        for i in range(1, len(array)):
            for j in range(1, len(array)):
                sum[i] += int(array[i][j])

        # MODULES

        # array of files
        # FIXME
        file_array = []
        for i in range(0, len(x)-1):
            for j in range(0, len(x)-1):
                if x[i][j] not in file_array:
                    file_array.append(x[i][j])

        # array of modules
        module_array = []
        for i in range(0, len(array[0])):
            module_array.append(array[0][i])

        file_sum = 0
        for i in range(1, len(array)):
            if file_sum <= len(file_array) - 1:
                file_sum += 1
            for j in range(1, len(array)):
                if i != j and array[i][j] != "0":
                    graphx.add_edge(array[i][0] + "\n" + str(sum[i]), array[0][j] + "\n" + str(sum[j]),
                                    length=array[i][j])

                    graphx.add_edge(file_array[j], array[i][0] + "\n" + str(sum[i]), length="")

        # METHODS
        for i in range(1, len(array)):
            if len(array2[i - 1]) > 0:
                for j in range(0, len(array2[i - 1])):
                    graphx.add_edge(array2[i - 1][j], array[i][0] + "\n" + str(sum[i]), length="")

        # Connecting file to modules
        # graphx.add_edge(x[0][0], array[0][1], length="")

        color_map = []
        for node in graphx:
            if ".py" not in node:
                color_map.append('lightblue')
            elif ".py\n(" not in node:
                color_map.append('lightgreen')
            else:
                color_map.append('#fff989')

        plt.title("Version: " + getVer())
        pos = nx.spring_layout(graphx)
        nx.draw(graphx, pos, edge_color='black', width=0.5, node_size=1000, node_color=color_map, with_labels=True,
                font_size=10)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in graphx.edges(data=True)])
        nx.draw_networkx_edge_labels(graphx, pos, edge_labels=edge_labels, label_pos=0.4)
        plt.show()

    # Story 6
    def draw_file_method_graph_direct(self):

        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)

        array = module_graph_gen.get_graph()[0]
        array2 = module_graph_gen.get_graph()[1]

        plt.figure(figsize=(12, 12))
        graphx = nx.DiGraph()
        for i in range(1, len(array)):
            graphx.add_node(array[i][0])

        for i in range(1, len(array)):
            if len(array2[i - 1]) > 0:
                for j in range(0, len(array2[i - 1])):
                    graphx.add_edge(array2[i - 1][j], array[i][0])

        color_map = []
        for node in graphx:
            if ".py" not in node:
                color_map.append('lightblue')
            else:
                color_map.append('#fff989')
                1
        plt.title("Version: " + getVer())
        pos = nx.planar_layout(graphx)
        nx.draw(graphx, pos, edge_color='black', width=0.5, node_size=1000, node_color=color_map, with_labels=True,
                font_size=10)
        plt.show()

