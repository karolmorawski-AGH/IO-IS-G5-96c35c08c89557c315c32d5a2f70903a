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
    print(path)
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
   
def get_graph(directory):
    files = []
    dependency_array = []
    #Getting all available local user-defined .py files
    for file in os.listdir(directory):
        if filter_non_py(file) == 1:
            files.append(file[:-3])

    for file in os.listdir(directory):
        if filter_non_py(file) == 1:
            for imp in get_imports(directory + "/" + file):
                if str(imp[0]) == "[]":
                    module = str(imp[1])
                    module = module[2:-2]
                    if module in files:
                        dependency_array.append([file  + "\n(" + str(os.stat(directory + "/" + file).st_size) + ")", module + ".py\n(" + str(os.stat(directory + "/" + module + ".py").st_size) + ")", count_func(directory + "/" + module + ".py")])
                else:
                    module = str(imp[0])
                    module = module[2:-2]
                    if module in files:
                        dependency_array.append([file  + "\n(" + str(os.stat(directory + "/" + file).st_size) + ")", module + ".py\n(" + str(os.stat(directory + "/" + module + ".py").st_size) + ")", 1])
 
    return dependency_array

#Getting func/methods names
def show_info(functionNode, funcArray):
    funcArray.append(functionNode.name)

#Getting func/methods names DECLARED
def get_func_list(filepath):

    #array of func/methods for given sfile
    func_array = []
    func_array.append(filepath[:-3])
    filename = filepath
    with open(filename) as file:
        node = ast.parse(file.read())

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]

    for function in functions:
        show_info(function, func_array)
    
    return func_array

def get_graph_func(directory):
    files = []
    declared_f = []
    called_f = []
    #Getting all available local user-defined .py files
    for file in os.listdir(directory):
        if filter_non_py(file) == 1:
            files.append(file[:-3])
    
    for file in os.listdir(directory):
        declared_f.append(get_func_list(file))
        called_f.append(list_func_calls(file))
    #Called funcs                   
    '''
    print("Declared:\n\n")
    i = 0
    while i < len(declared_f):
        print(declared_f[i])
        i = i + 1
    print("\n\nCalled:\n")
    i = 0
    while i < len(called_f):
        print(called_f[i])
        i = i + 1
    '''

    w = len(called_f) + 1
    h = len(declared_f) + 1
    Matrix = [["" for x in range(w)] for y in range(h)] 


    module_array = []
    i = 0
    while i < len(declared_f):
        module_array.append(declared_f[i][0])
        i = i + 1


    i = 1
    while i <  len(module_array)+1:
        Matrix[0][i] = module_array[i-1]
        i = i + 1

    i = 1
    while i <  len(module_array)+1:
        Matrix[i][0] = module_array[i-1]
        i = i + 1
            
    i = 1
    while i < len(Matrix[0]):
        j = 1
        while j < len(Matrix):
            if i == j:
                Matrix[i][j] = "0"
            else:
                #calling, declared
                #print(i,j, Matrix[i][0], Matrix[j][0])
                Matrix[i][j] = get_number_of_calls(Matrix[i][0], Matrix[j][0], called_f, declared_f)
            j = j+1
        i=i+1


    print(Matrix)


def get_number_of_calls(calling, declared, called_f, declared_f):
    
    #find calling array
    #print(called_f)
    call_desired = []
    i = 0
    while i < len(called_f):
        if called_f[i][0] == calling:
            call_desired = called_f[i]
        i = i + 1

    declared_desired = []
    i = 0
    while i < len(declared_f):
        if declared_f[i][0] == declared:
            declared_desired = declared_f[i]
        i = i + 1
    
    #TODO count how much from call_desired names matches declared desired

    return "-1"


from collections import deque

class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


#Getting func/methods names CALLED
def list_func_calls(filename):

    tree = ast.parse(open(filename).read())

    func_calls = [filename[:-3]]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls


#print(list_func_calls("graphgen.py"))
#list_func_calls("drawGraph", "pgraphdraw.py")
#print(inspect.stack()[1].function)
#pythonw -m trace -l graphgen.py 
get_graph_func("./")
