import unittest
import sys
sys.path.append('../')
from src.ioproject import DrawGraph
from src.ioproject import FileGraphGenerator

class TestDrawGraph(unittest.TestCase):
    directory =gs.dirpath
    if len(sys.argv) > 1:
        directory = sys.argv[1]

    def setUp(self):
        self.dgraph = DrawGraph(self.directory)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.dgraph.dirpath, self.directory)
    def test_draw_file_graph(self):
        pass
    def test_draw_method_graph(self):
        pass
    def test_draw_module_graph(self):
        pass
    def test_draw_file_module_graph(self):
        pass
    def test_draw_file_method_graph_direct(self):

        pass


if __name__ == '__main__':
    unittest.main()