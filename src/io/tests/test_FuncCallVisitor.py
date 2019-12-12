import unittest
import sys
sys.path.append('../')
from graph_generator import FuncCallVisitor


class TestFuncCallVisitor(unittest.TestCase):

    def setUp(self):
        self.funccv = FuncCallVisitor()

    def tearDown(self):
        pass

    def test_init(self):
        pass

    def test_name(self):
        pass

    def test_visit_Name(self):
        pass

    def test_visit_Attribute(self):
        pass

if __name__ == '__main__':
    unittest.main()