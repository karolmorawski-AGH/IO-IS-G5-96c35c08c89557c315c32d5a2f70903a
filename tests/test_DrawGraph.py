import unittest
import sys
sys.path.append('../')
from src.ioproject import DrawGraph
from src.ioproject import FileGraphGenerator
import src.ioproject.graph_generator as gg
import src.ioproject.graph_sketcher as gs

class TestDrawGraph(unittest.TestCase):
    directory = "./"
    if len(sys.argv) > 1:
        directory = sys.argv[1]

    def setUp(self):
        self.dgraph = DrawGraph(self.directory)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.dgraph.dirpath, self.directory)

    def test_draw_file_graph(self):
        self.assertEqual(gs.file_graph_gen, gg.FileGraphGenerator(self.directory))


    def test_draw_method_graph(self):
        self.assertEqual(gs.module_graph_gen , gg.ModuleGraphGenerator(self.directory))

    def test_draw_module_graph(self):
        pass

    def test_draw_file_module_graph(self):
        self.assertFalse(gs.color_map.append(23435235))
        self.assertFalse(gs.color_map.append('%#%!536'))


    def test_draw_file_method_graph_direct(self):
        pass

if __name__ == '__main__':
    unittest.main()