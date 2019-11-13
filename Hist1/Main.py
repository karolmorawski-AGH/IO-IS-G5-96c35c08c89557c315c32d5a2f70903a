import pgraphdraw as pg
import pdepgen as pd
import sys

# Default directory
DIR = "./"
# If called with args then use those args as parameters for DIR
if len(sys.argv)>1:
    directory = sys.argv[1]

graph_representation = pd.GraphGenerator("./")
print(graph_representation.get_graph())

#pg.drawGraph(dependency_array)
