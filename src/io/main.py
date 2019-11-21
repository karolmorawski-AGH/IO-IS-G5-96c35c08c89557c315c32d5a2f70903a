import graph_sketcher as pg
import graph_generator as pd
import sys

directory = "./"
if len(sys.argv)>1:
    directory = sys.argv[1]

dependency_array = pd.get_graph_func(directory)
pg.draw_graph(dependency_array)
