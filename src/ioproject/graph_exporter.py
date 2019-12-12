import src.ioproject.graph_generator
import abc

# This module contains all classes and methods needed for graph export to Visual Paradigm

# Interface
class IGraphExporter(abc.ABC):
    # Exports graph as xml/excel(?)
    @abc.abstractmethod
    def export_graph(self, path, filename):
        pass

    # Filename for exported graph
    @property
    def path(self):
        raise NotImplementedError

    # Default path to desired directory with modules (default is current directory)
    @property
    def filename(self):
        raise NotImplementedError