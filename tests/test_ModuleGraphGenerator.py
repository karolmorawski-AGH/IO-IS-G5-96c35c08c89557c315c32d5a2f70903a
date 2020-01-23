import unittest
import sys
sys.path.append('../')
from src.ioproject import ModuleGraphGenerator

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
        pass

    def test_get_graph(self):
        self.assertTrue(self.modulegg.get_graph())
        pass

    def test_filter_non_py(self):
        self.assertFalse(self.modulegg.filter_non_py(self.dirpath))
        pass

    def test_get_func_list(self):
        pass

    def test_list_func_calls(self):
        pass

    def test_get_number_of_calls(self):
        pass

    def test_show_info(self):
        pass

if __name__ == '__main__':
    unittest.main()