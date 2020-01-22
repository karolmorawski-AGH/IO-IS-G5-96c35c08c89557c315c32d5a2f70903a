import unittest
import sys
sys.path.append('../')
from src.ioproject import FileGraphGenerator
import src.ioproject.graph_generator as gg
class TestFileGraphGenerator(unittest.TestCase):
    dirpath = "./"

    def setUp(self):
        self.filegg = FileGraphGenerator(self.dirpath)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.filegg.dirpath, self.dirpath)

    def test_get_graph(self):
        self.assertTrue(gg.files)
        self.assertTrue(gg.dependency_array)
        pass

    def test_filter_non_py(self):
        s = "AAA/BBB/CCC/d.py"
        d = "AAA/BBB/CCC/d.x"
        f = "123qwe"
        self.assertTrue(gg.filter_non_py(s))
        self.assertFalse(gg.filter_non_py(d))
        self.assertFalse(gg.filter_non_py(f))
        pass
    def test_get_imports(self):
        pass

    def test_count_func(self):
        self.assertFalse(gg.sum<0)
        self.assertTrue(gg.node)
        pass

if __name__ == '__main__':
    unittest.main()
