import traitlets as T

import ipywidgets as W
import networkx as nx
from rdflib import Graph


class VisBase(W.VBox):
    graph = T.Instance(Graph, allow_none=True)
    _vis = T.Instance(W.Box, allow_none=True)
    edge_color = T.Unicode()
    node_color = T.Unicode()
    selected_nodes = T.List()
    selected_edges = T.List()
    hovered_nodes = T.List()
    hovered_edges = T.List()

    layouts = {
        "circular_layout": nx.layout.circular_layout,
        "random_layout": nx.layout.random_layout,
        "shell_layout": nx.layout.shell_layout,
        "spring_layout": nx.layout.spring_layout,
        "spiral_layout": nx.layout.spiral_layout,
    }

    @T.default("edge_color")
    def _make_default_edge_color(self):
        return "pink"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edge_color = kwargs.get("edge_color", "pink")
        self.node_color = kwargs.get("node_color", "grey")
        self.graph = kwargs.get("graph", None)
        self.nx_layout = self.layouts[kwargs.get("nx_layout", "circular_layout")]
