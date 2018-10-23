"""Visiting nodes of ASTs"""


import ast
import linecache


class PymVisitor(ast.NodeVisitor):
    """ABC for all pym's Vistors"""
    def __init__(self):
        super(PymVisitor, self).__init__()

    def generic_visit(self, node):
        raise NotImplementedError('Cannot visit %s' % node.__class__.__name__)


class Sourcer(PymVisitor):
    def __init__(self):
        super(Sourcer, self).__init__()

    def generic_visit(self, node):
        line_number = node.lineno
        line = linecache.getline(filename, line_number).rstrip()


class Liner(PymVisitor):
    def __init__(self):
        super(Liner, self).__init__()
        self._old = None
        self.lines = {}

    def generic_visit(self, node):
        number = node.lineno
        try:
            first = self.lines[number][0]
            self.lines[number] = (first, node)
        except KeyError:
            self.lines[number] = (node, node)
