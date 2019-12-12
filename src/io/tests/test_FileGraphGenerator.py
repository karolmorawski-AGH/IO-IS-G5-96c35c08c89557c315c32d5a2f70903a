import unittest
import sys
sys.path.append('../')
from graph_generator import FileGraphGenerator

class TestFileGraphGenerator(unittest.TestCase):
    dirpath = "./"

    def setUp(self):
        self.filegg = FileGraphGenerator(self.dirpath)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.filegg.dirpath, self.dirpath)

    def test_get_graph(self):
        pass

    def test_filter_non_py(self):
        pass

    def test_get_imports(self):
        pass

    def test_count_func(self):
        pass

if __name__ == '__main__':
    unittest.main()