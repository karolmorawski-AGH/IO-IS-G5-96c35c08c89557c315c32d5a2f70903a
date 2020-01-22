import os
import ast
import abc
import sys
from collections import namedtuple
from collections import deque


# This module contains all classes and methods needed to create appropriate graph representation
# then graph_sketcher handles drawing graphical representation of graph

# Interface
class IGraphGenerator(abc.ABC):
    # Returns graph representation for use in Sketcher
    @abc.abstractmethod
    def get_graph(self):
        pass

    # Default path to desired directory with modules (default is current directory)
    @property
    def dirpath(self):
        raise NotImplementedError


# File relationship graph (1)
class FileGraphGenerator(IGraphGenerator):
    dirpath = ""
    # Tuple for get_imports
    importHelper = namedtuple("Import", ["module", "name", "alias"])

    # Constructor
    def __init__(self, dirpath):
        self.dirpath = dirpath

    # Returns graph representation for use in Sketcher
    def get_graph(self):
        files = []
        dependency_array = []
        # Getting all available local user-defined .py files
        for file in os.listdir(self.dirpath):
            if self.filter_non_py(file) == 1 and os.path.isdir(file) is not True:
                files.append(file[:-3])
        # This loop is self-explanatory
        for file in os.listdir(self.dirpath):
            # Filtering out directories
            if os.path.isdir(file) is not True:
                if self.filter_non_py(file) == 1:
                    for imp in self.get_imports(self.dirpath + "/" + file):
                        if str(imp[0]) == "[]":
                            module = str(imp[1])
                            module = module[2:-2]
                            if module in files:
                                dependency_array.append(
                                    [file + "\n(" + str(os.stat(self.dirpath + "/" + file).st_size) + ")",
                                     module + ".py\n(" + str(
                                         os.stat(self.dirpath + "/" + module + ".py").st_size) + ")",
                                     self.count_func(self.dirpath + module + ".py")])
                        else:
                            module = str(imp[0])
                            module = module[2:-2]
                            if module in files:
                                dependency_array.append(
                                    [file + "\n(" + str(os.stat(self.dirpath + "/" + file).st_size) + ")",
                                     module + ".py\n(" + str(
                                         os.stat(self.dirpath + "/" + module + ".py").st_size) + ")", 1])

        return dependency_array

    # Filters non-source code files
    @staticmethod
    def filter_non_py(path):
        if ".py" in path:
            return 1
        elif ".pyc" in path:
            return 0
        else:
            return 0

    # Returns all imported modules with aliases
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
                yield self.importHelper(module, n.name.split('.'), n.asname)

    # Counts number of functions and methods in given module
    def count_func(self, module):

        module = module.split("/")[-1]

        with open(module) as file:
            tree = ast.parse(file.read())

        sum = 0
        node = ast.NodeVisitor
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if (node.name == "__init__"):
                    pass
                else:
                    sum += 1

        return sum


# Method relationship graph (2)
class MethodGraphGenerator(IGraphGenerator):
    dirpath = ""

    # Constructor
    def __init__(self, dirpath):
        self.dirpath = dirpath

    # Returns graph representation for use in Sketcher
    def get_graph(self):
        files = []
        declared_f = []

        # Saving all available local user-defined .py files to files[]
        for file in os.listdir(self.dirpath):
            if ModuleGraphGenerator.filter_non_py(file) == 1 and file and os.path.isdir(file) is not True:
                files.append(file[:-3])

        # Dokumentacja w komentarzu
        # Only declared functions/methods are considered. The goal is to generate dirgraph representation
        # where edge values are number of calls to a function/method from another function/method
        # Calls from __main__ not to be considered.
        #                           C A L L E D             node value
        #                        fun1()  fun2()  fun3()     _________
        #      DEC-          fun1()   0       2       5     2+5+0 = 7
        #      LARED         fun2()   1       1       0     1+1+0 = 2
        #                    fun3()   2       0       0     2+0+0 = 2
        #
        # Declared functions/methods are essentially graph nodes and node values are calculated as pictured above.

        # Getting all declared functions
        for file in os.listdir(self.dirpath):
            if os.path.isdir(file) is not True:
                declared_f.append(ModuleGraphGenerator.get_func_list(file))

        graph = self.get_representation(declared_f, files)
        return graph


    # Generating blank graph representation
    def get_representation(self, declared_f, file_list):

        # Sanitizing and concatenating declared_f
        i = 0
        while i < len(declared_f):
            # Checking for files with no function calls
            if len(declared_f[i]) == 1:
                declared_f.pop(i)
                # Correcting indexes tracking
                i -= 1
            i += 1

        i = 0
        while i < len(declared_f):
            declared_f[i].pop(0)
            i += 1

        declared_list = [item for sublist in declared_f for item in sublist]
        declared_list = list(dict.fromkeys(declared_list))
        graph = [["" for x in range(len(declared_list))] for y in range(len(declared_list))]

        i = 1
        while i < len(declared_list):
            graph[0][i] = declared_list[i]
            i = i + 1

        i = 1
        while i < len(declared_list):
            graph[i][0] = declared_list[i]
            i = i + 1

        # Calculating edge values
        i = 1
        while i < len(graph):
            j = 1
            while j < len(graph[i]):
                graph[i][j] = self.set_calls(graph[i][0], graph[j][0], declared_f, file_list)
                j = j + 1
            i = i + 1
        return graph

    @staticmethod
    def set_calls(object_function, target_function, declared_f, file_list):

        if '__init__' in file_list:
            file_list.remove('__init__')
        # Associating object function with it's file in which it is declared
        # Bardzo optymistyczne zalozenie ze file_list oraz declared_f jest po kolei
        file = ''
        try:
            i = 0
            while i < len(declared_f):
                if object_function in declared_f[i]:
                    file = file_list[i]
                i += 1
            if file == '':
                raise FileNotFoundError('Object function is not present in declared functions list')
        except FileNotFoundError as e:
            print(e)
            return 0

        # Iterator of func calls
        num_of_calls = 0
        file = file + '.py'
        loc_range = [0, -1]

        with open(file) as source_code:
            p = ast.parse(source_code.read())

        node = ast.NodeVisitor
        # Walking through nodes searching for method definition and getting its first line

        for node in ast.walk(p):
            if isinstance(node, ast.FunctionDef):
                if node.name == object_function:
                    loc_range[0] = node.lineno
                    break

        # Iterating through file lines and checking indents to determine method definition last line
        line_iterator = 1
        indent_offset = 0
        with open(file) as source_code:
            for line in source_code:
                if line == '':
                    continue
                if line_iterator == loc_range[0]:
                    # Getting indent
                    indent_offset = len(line) - len(line.lstrip())
                    # No all edge cases considered - if method is nested inside one class it may jump to first indented
                    # line in second class and EOF may be actually as def of method or variable (but that's fine)
                if (len(line) - len(line.lstrip())) == indent_offset and line_iterator > loc_range[0]:
                    loc_range[1] = line_iterator
                    break
                line_iterator += 1

        num_of_calls = MethodGraphGenerator.find_calls(file, target_function, loc_range[0], loc_range[1])

        return num_of_calls

    # Finds number of calls of a function/method in given fragment of source code
    @staticmethod
    def find_calls(file, target_function, start, end):
        num_of_calls = 0
        with open(file) as f:
            for line in f.readlines()[start:end]:
                # Sanitizing line to remove strings nad eliminate false-positives
                line_t = line.join(line.rsplit('"', 1))[1:]
                if MethodGraphGenerator.is_call(line, target_function):
                    num_of_calls += line.count(target_function + '(')

        return num_of_calls

    # Checks if string is a method/function call and returns number of calls in that line
    @staticmethod
    def is_call(line, target_function):
        # Some quality code here
        if target_function + "(" in line and 'def ' not in line:
            return True

        return False

    # Prints graph
    def print_representation(self, graph):
        i = 0
        while i < len(graph):
            print(graph[i])
            i += 1


# Module relationship graph (3)
class ModuleGraphGenerator(IGraphGenerator):
    dirpath = ""

    # Constructor
    def __init__(self, dirpath):
        self.dirpath = dirpath

    def get_files(self):
        files = []
        for file in os.listdir(self.dirpath):
            if self.filter_non_py(file) == 1:
                files.append(file[:])
        return files

    # Returns graph representation for use in Sketcher
    def get_graph(self):
        files = []
        declared_f = []
        called_f = []
        # Getting all available local user-defined .py files
        for file in os.listdir(self.dirpath):
            if os.path.isdir(file) is not True:
                if self.filter_non_py(file) == 1:
                    files.append(file[:-3])

        for file in os.listdir(self.dirpath):
            if os.path.isdir(file) is not True:
                declared_f.append(self.get_func_list(file))
                called_f.append(self.list_func_calls(file))

        w = len(called_f) + 1
        h = len(declared_f) + 1
        Matrix = [["" for x in range(w)] for y in range(h)]

        module_array = []
        i = 0
        while i < len(declared_f):
            module_array.append(declared_f[i][0])
            i = i + 1

        i = 1
        while i < len(module_array) + 1:
            Matrix[0][i] = module_array[i - 1]
            i = i + 1

        i = 1
        while i < len(module_array) + 1:
            Matrix[i][0] = module_array[i - 1]
            i = i + 1

        i = 1
        while i < len(Matrix):
            j = 1
            while j < len(Matrix[i]):
                if i == j:
                    Matrix[i][j] = "0"
                else:
                    # calling, declared
                    Matrix[i][j] = self.get_number_of_calls(Matrix[i][0], Matrix[j][0], called_f, declared_f)
                j = j + 1
            i = i + 1

        # Removing first index of declared functions - frontend requirement
        i = 0
        while i < len(declared_f):
            declared_f[i].pop(0)
            i = i + 1

        # Adding '.py' to module names - frontend requirement - useless
        i = 1
        while i < len(Matrix):
            # since directional graph representation in this case is square matrix no j iterator
            Matrix[0][i] = Matrix[0][i] + ".py"
            Matrix[i][0] = Matrix[i][0] + ".py"
            i = i + 1

        returnedMatrix = []
        returnedMatrix.append(Matrix)
        returnedMatrix.append(declared_f)
        return returnedMatrix

    # Filters non-source code files
    @staticmethod
    def filter_non_py(path):
        if ".py" in path:
            return 1
        elif ".pyc" in path:
            return 0
        else:
            return 0

    # Getting func/methods names DECLARED
    @staticmethod
    def get_func_list(filepath):

        # array of func/methods for given file
        func_array = []
        filename = filepath
        filepath = filepath.split("/")[-1]
        func_array.append(filepath[:-3])

        with open(filename) as file:
            p = ast.parse(file.read())

        node = ast.NodeVisitor
        for node in ast.walk(p):
            if isinstance(node, ast.FunctionDef):
                if (node.name in func_array):
                    pass
                else:
                    func_array.append(node.name)

        return func_array

    # Getting func/methods names CALLED
    @staticmethod
    def list_func_calls(filename):

        tree = ast.parse(open(filename).read())

        func_calls = [filename[:-3]]
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                callvisitor = FuncCallVisitor()
                callvisitor.visit(node.func)
                func_calls.append(callvisitor.name)

        return func_calls

    @staticmethod
    def get_number_of_calls(calling, declared, called_f, declared_f):

        # find calling array
        call_desired = []
        i = 0
        while i < len(called_f):
            if called_f[i][0] == calling:
                call_desired = called_f[i]
                break
            i = i + 1

        # Removing module aliases in func calls
        i = 0
        while i < len(call_desired):
            if '.' in call_desired[i]:
                call_desired[i] = call_desired[i].split(".")[1]
            i = i + 1

        declared_desired = []
        i = 0
        while i < len(declared_f):
            if declared_f[i][0] == declared:
                declared_desired = declared_f[i]
                break
            i = i + 1

        i = 0
        calls_num = 0;
        while i < len(call_desired):
            if call_desired[i] in declared_desired:
                calls_num = calls_num + 1
            i = i + 1

        return str(calls_num)

    # Getting func/methods names
    @staticmethod
    def show_info(functionNode, funcArray):
        funcArray.append(functionNode.name)


# Helper class for generating call graph
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

a = MethodGraphGenerator('./')
a.get_graph()
