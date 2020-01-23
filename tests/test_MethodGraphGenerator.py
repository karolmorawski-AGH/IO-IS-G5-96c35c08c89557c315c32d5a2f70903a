import unittest
import sys
sys.path.append('../')
from src.ioproject.graph_generator import MethodGraphGenerator

class TestMethodGraphGenerator(unittest.TestCase):
    dirpath = "./"
    def setUp(self):
        self.method = MethodGraphGenerator(self.dirpath)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.method.dirpath, self.dirpath)
        pass

    def test_get_graph(self):
        self.assertTrue(self.method.get_graph())


if __name__ == '__main__':
    unittest.main()