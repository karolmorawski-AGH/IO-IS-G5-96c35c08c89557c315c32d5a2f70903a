import os
import sys
import ast
from collections import namedtuple
from  itertools import chain

def count_func(filename):
    with open(filename) as f:
        tree = ast.parse(f.read())
        return sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

def filter_non_py(path):
    if ".py" in path:
        return 1
    else:
        return 0

Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
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
            yield Import(module, n.name.split('.'), n.asname)
   
def get_graph():
    files = []
    dependency_array = []
    #Getting all available local user-defined .py files
    for file in os.listdir("./"):
        if filter_non_py(file) == 1:
            files.append(file[:-3])

    for file in os.listdir("./"):
        if filter_non_py(file) == 1:
            for imp in get_imports(file):
                if str(imp[0]) == "[]":
                    module = str(imp[1])
                    module = module[2:-2]
                    if module in files:
                        dependency_array.append([file  + "\n(" + str(os.stat(file).st_size) + ")", module + ".py\n(" + str(os.stat(module + ".py").st_size) + ")", count_func(module+".py")])
                else:
                    module = str(imp[0])
                    module = module[2:-2]
                    if module in files:
                        dependency_array.append([file  + "(" + str(os.stat(file).st_size) + ")", module + ".py\n(" + str(os.stat(module + ".py").st_size) + ")", 1])
    
    return dependency_array