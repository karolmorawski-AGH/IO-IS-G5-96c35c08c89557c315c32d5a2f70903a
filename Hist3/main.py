import pgraphdraw as pg
import graphgen as pd
import sys

directory = "./"
if len(sys.argv)>1:
    directory = sys.argv[1]

dependency_array = pd.get_graph_func(directory)
#print(dependency_array)
pg.drawGraph(dependency_array)
