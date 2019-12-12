import unittest
import sys
sys.path.append('../')
from graph_generator import MethodGraphGenerator

class TestMethodGraphGenerator(unittest.TestCase):
    dirpath = "./"

    def setUp(self):
        self.methodgg = MethodGraphGenerator()

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.methodgg.dirpath, self.dirpath)

    def test_get_graph(self):
        pass

if __name__ == '__main__':
    unittest.main()