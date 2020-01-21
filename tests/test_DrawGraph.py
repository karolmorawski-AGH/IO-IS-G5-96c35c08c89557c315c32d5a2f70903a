import unittest
import sys
sys.path.append('../')
from src.ioproject import DrawGraph
from src.ioproject import FileGraphGenerator
import src.ioproject.graph_generator as gg
import src.ioproject.graph_sketcher as gs
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
        self.assertEqual(gs.file_graph_gen, gg.FileGraphGenerator(self.directory))
        self.assertTrue(gs.x)
        self.assertTrue(gs.G)
        self.assertTrue(gs.pos)
        self.assertTrue(gs.edge_labels)

    def test_draw_method_graph(self):
        self.assertEqual(gs.method_graph,gg.MethodGraphGenerator(self.directory))
        self.assertEqual(gs.module_graph_gen , gg.ModuleGraphGenerator(self.directory))
        self.assertTrue(gs.graph)
        self.assertTrue(gs.func)
        self.assertTrue(gs.fileCode)
        self.assertTrue(gs.complex)
        self.assertTrue(gs.G)
        self.assertTrue(gs.pos)
        self.assertTrue(gs.edge_labels)
    def test_draw_module_graph(self):
        self.assertEqual(gs.module_graph_gen,gg.ModuleGraphGenerator(self.directory))
        self.assertTrue(gs.array)
        self.assertTrue(gs.array2)
        self.assertTrue(gs.graphx)
        self.assertTrue(gs.sum>0)
        self.assertFalse(gs.color_map.append(23435235))
        self.assertFalse(gs.color_map.append('%#%!536'))
        self.assertTrue(gs.pos)
        self.assertTrue(gs.edge_labels)
        pass

    def test_draw_file_module_graph(self):
        self.assertEqual(gs.module_graph_gen,gg.ModuleGraphGenerator(self.directory))
        self.assertEqual(gs.file_graph_gen,gg.FileGraphGenerator(self.directory))
        self.assertTrue(gs.x)
        self.assertTrue(gs.array)
        self.assertTrue(gs.array2)
        self.assertTrue(gs.graphx)
        self.assertTrue(gs.sum>0)
        self.assertTrue(gs.file_array)
        self.assertFalse(gs.file_sum<0)
        self.assertTrue(gs.module_array)
        self.assertFalse(gs.color_map.append(23435235))
        self.assertFalse(gs.color_map.append('%#%!536'))
        self.assertTrue(gs.pos)
        self.assertTrue(gs.edge_labels)

    def test_draw_file_method_graph_direct(self):
        self.assertEqual(gs.module_graph_gen,gg.ModuleGraphGenerator(self.directory))
        self.assertTrue(gs.array)
        self.assertTrue(gs.array2)
        self.assertTrue(gs.graphx)
        self.assertFalse(gs.color_map.append(23435235))
        self.assertFalse(gs.color_map.append('%#%!536'))
        self.assertTrue(gs.pos)
        pass


if __name__ == '__main__':
    unittest.main()
