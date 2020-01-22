import unittest
import sys
import os
sys.path.append('../')
from src.ioproject import FileGraphGenerator
class TestFileGraphGenerator(unittest.TestCase):
    dirpath = "./"

    def setUp(self):
        self.filegg = FileGraphGenerator(self.dirpath)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.filegg.dirpath, self.dirpath)

    def test_get_graph(self):

        self.assertTrue(self.filegg.get_graph())

    def test_filter_non_py(self):
        s = "AAA/BBB/CCC/d.py"
        d = "AAA/BBB/CCC/d.x"
        f = "123qwe"
        self.assertTrue(self.filegg.filter_non_py(s))
        self.assertFalse(self.filegg.filter_non_py(d))
        self.assertFalse(self.filegg.filter_non_py(f))
    def test_get_imports(self):
        x=self.filegg.importHelper
        file=[]
        file=os.listdir(self.dirpath)
        y=self.filegg.get_imports(self.dirpath + "/" + file[0])
        self.assertFalse(x==y)

    def test_count_func(self):
        self.assertFalse(self.dirpath.count_func("test_DrawGraph.py")<0)

if __name__ == '__main__':
    unittest.main()