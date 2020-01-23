import unittest
import sys
sys.path.append('../')
from src.ioproject.graph_generator import ModuleGraphGenerator

class TestModuleGraphGenerator(unittest.TestCase):
    dirpath = "./"

    def setUp(self):
        self.modulegg = ModuleGraphGenerator(self.dirpath)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.modulegg.dirpath, self.dirpath)

    def test_get_files(self):
        file=[]
        self.assertFalse(self.modulegg.get_files()==file)

    def test_get_graph(self):
        self.assertTrue(self.modulegg.get_graph())

    def test_filter_non_py(self):
        self.assertFalse(self.modulegg.filter_non_py(self.dirpath))

    def test_get_func_list(self):
        filepath = "./test_ModuleGraphGenerator.py"
        func_array = ["test_ModuleGraphGenerator", "setUp", "tearDown", "test_init", "test_get_files", "test_get_graph", "test_filter_non_py", "test_get_func_list", "test_list_func_calls", "test_get_number_of_calls", "test_show_info"]
        self.assertEqual(func_array,self.modulegg.get_func_list(filepath))

    def test_list_func_calls(self):
        filepath = "./test_ModuleGraphGenerator.py"
        func_array2 = ['test_ModuleGraphGenerator',
 'setUp',
 'tearDown',
 'test_init',
 'test_get_files',
 'test_get_graph',
 'test_filter_non_py',
 'test_get_func_list',
 'test_list_func_calls',
 'test_get_number_of_calls',
 'test_show_info']
        self.assertEqual(func_array2,self.modulegg.get_func_list(filepath))

    def test_get_number_of_calls(self):
        pass

    def test_show_info(self):
        pass

if __name__ == '__main__':
    unittest.main()
