import networkx as nx
import matplotlib.pyplot as plt
import graph_generator as gg


# This module contains DrawGraph class with methods corresponding to drawing specific type of graph
# Uses graph_generator module methods for getting graph representations and then interprets them
# accordingly

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

        G = nx.DiGraph()
        for i in range(0, len(x)):
            G.add_edge(x[i][0], x[i][1], length=x[i][2])

        pos = nx.spring_layout(G)
        nx.draw(G, pos, edge_color='black', width=1, node_size=1000, node_color='lightgreen', with_labels=True)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
        plt.show()

    # Draws method relationship graph
    def draw_method_graph(self):
        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)
        files = module_graph_gen.get_files()
        func = []
        for i in range(0,len(files)):
            func+=module_graph_gen.get_func_list(files[i])

        G = nx.DiGraph()
        for i in range(0, len(func)):
            G.add_node(func[i])
        pos = nx.spring_layout(G)
        nx.draw(G, pos, edge_color='black', width=1, node_size=1000, node_color='lightblue', with_labels=True)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)
        plt.show()




    # Draws file relationship graph

    def draw_module_graph(self):

        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)

        array = module_graph_gen.get_graph()[0]
        array2 = module_graph_gen.get_graph()[1]

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

        pos = nx.spring_layout(graphx)
        nx.draw(graphx, pos, edge_color='black', width=0.5, node_size=1000, node_color=color_map, with_labels=True, font_size=10)
        edge_labels = dict([((u, v,), d['length']) for u, v, d in graphx.edges(data=True)])
        nx.draw_networkx_edge_labels(graphx, pos, edge_labels=edge_labels, label_pos=0.4)
        plt.show()


    # File + Module graph
    def draw_file_module_graph(self):
        module_graph_gen = gg.ModuleGraphGenerator(self.dirpath)
        file_graph_gen = gg.FileGraphGenerator(self.dirpath)

        x = file_graph_gen.get_graph()
        array = module_graph_gen.get_graph()[0]
        array2 = module_graph_gen.get_graph()[1]

        graphx = nx.MultiDiGraph()

        # FOR module graph
        sum = [0] * len(array)

        for i in range(1, len(array)):
            for j in range(1, len(array)):
                sum[i] += int(array[i][j])


        # MODULES

        # array of files
        file_array = []
        for i in range(0, len(x)):
            for j in range(0, len(x)):
                if x[i][j] not in file_array:
                    file_array.append(x[i][j])

        #array of modules
        module_array = []
        for i in range(0, len(array[0])):
            module_array.append(array[0][i])

        file_sum = 0
        for i in range(1, len(array)):
            if file_sum <= len(file_array)-1:
                file_sum+=1
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
        #graphx.add_edge(x[0][0], array[0][1], length="")




        color_map = []
        for node in graphx:
            if ".py" not in node:
                color_map.append('lightblue')
            elif ".py\n(" not in node:
                color_map.append('lightgreen')
            else:
                color_map.append('#fff989')

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
        graphx = nx.DiGraph()
        for i in range(1,len(array)):
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
                color_map.append('lightgreen')

        pos = nx.planar_layout(graphx)
        nx.draw(graphx, pos, edge_color='black', width=0.5, node_size=1000, node_color=color_map, with_labels=True, font_size=10)
        plt.show()



test = DrawGraph("./")
test.draw_file_module_graph()
