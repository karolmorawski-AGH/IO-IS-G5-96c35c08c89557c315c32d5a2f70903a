import os
import sys
import my_module
import ast
from collections import OrderedDict

#Zalozenie: wszystkie pliki w jednym katalogu
def count_func(filename):
    with open(filename) as f:
        tree = ast.parse(f.read())
        return sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

def filter_non_py(path):
    if ".py" in path:
        return 1
    else:
        return 0

def get_graph():

    dependency_array = []
    files = []

    #Getting all available modules which may be impoted by other modules
    for file in os.listdir("./"):
        if filter_non_py(file) == 1:
            files.append(file[:-3])
            #dependency_array.append([file + "\n(" + str(os.stat(file).st_size) + ")"])

    #Iterating through each module and trying to find 'impot x' or 'impot y from x'



    #xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
    for file in os.listdir("./"):
        if filter_non_py(file) == 1:
            #czytaj plik
            #znajdz 'impot' linie
            #wszystko po impot zapisuje
            #jesli jest w files to tablica  [cel(size), zrodlo(size), ilosc funkcji]
            #czyli                          [file(size), imported_module, ilosc_funkcji]
            with open(file) as fp:
                line = fp.readline()
                while line:
                    if line[:6] == "import":
                        dependency = line[7:]
                        dependency = dependency[:-1]

                        if dependency in files:
                        #print(file + " zalezy od " + line[7:])
                            dependency_array.append([file + "\n(" + str(os.stat(file).st_size) + ")", dependency, count_func(dependency+".py")])
                            
                    line = fp.readline()

    return dependency_array



#zwraca duplikaty
print(get_graph())