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


#Getting func/methods names CALLED
import dis
def list_func_calls(fn, file):
    
    import pgraphdraw

    fn = eval(fn)

    funcs = []
    bytecode = dis.Bytecode(fn)
    instrs = list(reversed([instr for instr in bytecode]))
    for (ix, instr) in enumerate(instrs):
        if instr.opname=="CALL_FUNCTION":
            load_func_instr = instrs[ix + instr.arg + 1]
            if load_func_instr.opname == "LOAD_GLOBAL":
                funcs.append(load_func_instr.argval)

    return funcs

def get_graph_func(directory):
    files = []
    declared_f = []
    called_f = []
    #Getting all available local user-defined .py files
    for file in os.listdir(directory):
        if filter_non_py(file) == 1:
            files.append(file[:-3])
    
    #Declared funcs
    for file in os.listdir(directory):
        declared_f.append(get_func_list(file))
        called_f.append(get_func_calls_list(file))

    #Called funcs                   

    #print("Declared:\n\n")
    #print(declared_f)
    #print("\n\nCalled:\n")
    #print(called_f)
    return 0

#THIS FUNCTION ALWAYS AS LAST FUNCTION IN FILE
def get_func_calls_list(file):
    f_number = len(get_func_list(file))
    tab = [file]
    i = 1 
    while i < f_number:
        print(get_func_list(file)[i])
        tab=tab+(list_func_calls(get_func_list(file)[i], file[:-3]))
        i = i + 1
    #print(tab)
    return tab

#print(inspect.stack()[1].function)
import subprocess
#pythonw -m trace -l graphgen.py 

result = subprocess.run(["python", "-m", "trace", "-l", "main.py"], stdout=subprocess.PIPE)
result.stdout