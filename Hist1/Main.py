import pgraphdraw as pg
import pdepgen as pd

dependency_array = pd.get_graph("../test/")
print(dependency_array)
pg.drawGraph(dependency_array)
