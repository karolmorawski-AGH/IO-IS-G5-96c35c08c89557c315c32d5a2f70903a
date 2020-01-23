import unittest
import sys

from _ast import Call

sys.path.append('../')
from src.ioproject.graph_generator import FuncCallVisitor
from collections import deque


class TestFuncCallVisitor(unittest.TestCase):

    def setUp(self):
        self.funccv = FuncCallVisitor()

    def tearDown(self):
        pass

    def test_init(self):
        self.assertTrue(isinstance(self.funccv.name, deque))

    def test_name(self):
        self.funccv._name.append("foo")
        self.funccv._name.append("baz")
        self.assertEqual(self.funccv.name, ".foobaz")

    def test_visit_Name(self):
        node = Call()
        node.id = "fname"
        self.funccv.visit_Name(node)
        self.assertEqual("".join(self.funccv._name), "fname")

    def test_visit_Attribute(self):
        node = Call()
        node.attr = "attr"
        node.value.id = "valueid"
        self.funccv.visit_Name(node)
        self.assertEqual("".join(self.funccv._name), "valueidattr")
