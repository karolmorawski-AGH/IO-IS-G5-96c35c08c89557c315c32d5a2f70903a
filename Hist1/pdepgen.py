import os
import sys
import ast
from collections import namedtuple
from itertools import chain


# Processes files in given directory and generates graph representation
class GraphGenerator:
    # Path to desired directory with modules (default is current directory)
    dirpath = "./"
    # Tuple for get_imports
    Import = namedtuple("Import", ["module", "name", "alias"])

    # Constructor
    def __init__(self, dirpath):
        self.dirpath = dirpath

        # Counts number of functions and methods in given module
    def count_func(self, module):
        with open(module) as f:
            tree = ast.parse(f.read())
            return sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

    # Filters out files not being modules (*.py files)
    def filter_non_py(self, path):
        if ".py" in path:
            return 1
        else:
            return 0

    # I guess it returns all imported modules with aliases idk
    def get_imports(self, path):
        with open(path) as fh:
            root = ast.parse(fh.read(), path)

        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module.split('.')
            else:
                continue

            for n in node.names:
                yield self.Import(module, n.name.split('.'), n.asname)

    # Generates and returns graph representation
    def get_graph(self):
        files = []
        dependency_array = []
        # Getting all available local user-defined .py files
        for file in os.listdir(self.dirpath):
            if self.filter_non_py(file) == 1:
                files.append(file[:-3])
        # This loop is self-explanatory
        for file in os.listdir(self.dirpath):
            if self.filter_non_py(file) == 1:
                for imp in self.get_imports(self.dirpath + "/" + file):
                    if str(imp[0]) == "[]":
                        module = str(imp[1])
                        module = module[2:-2]
                        if module in files:
                            dependency_array.append([file + "\n(" + str(os.stat(self.dirpath + "/" + file).st_size) + ")",
                                                     module + ".py\n(" + str(
                                                         os.stat(self.dirpath + "/" + module + ".py").st_size) + ")",
                                                     self.count_func(self.dirpath + "/" + module + ".py")])
                    else:
                        module = str(imp[0])
                        module = module[2:-2]
                        if module in files:
                            dependency_array.append([file + "\n(" + str(os.stat(self.dirpath + "/" + file).st_size) + ")",
                                                     module + ".py\n(" + str(
                                                         os.stat(self.dirpath + "/" + module + ".py").st_size) + ")", 1])

        return dependency_array