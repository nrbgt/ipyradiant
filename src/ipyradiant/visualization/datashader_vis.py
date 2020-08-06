import networkx as nx
import traitlets as T
import ipywidgets as W
from ipyradiant import LoadWidget
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import holoviews as hv
from holoviews.operation.datashader import datashade, bundle_graph, dynspread
import ipycytoscape
from bokeh.models import HoverTool
import bokeh.models.widgets as bk
import jupyter_bokeh as jbk
from bokeh.plotting import figure
from .base import VisBase

hv.extension("bokeh")


class DatashaderVis(VisBase):
    edge_tooltips = [
        ("Source", "@start"),
        ("Target", "@end"),
    ]
    edge_hover = HoverTool(tooltips=edge_tooltips)

    node_tooltips = [
        ("ID", "@index"),
    ]
    node_hover = HoverTool(tooltips=node_tooltips)
    sparql = """
        CONSTRUCT {
            ?s ?p ?o .
        }
        WHERE {
            ?s ?p ?o .
            FILTER (!isLiteral(?o))
            FILTER (!isLiteral(?s))
        }
        LIMIT 300
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tooltip = kwargs.get("tooltip", "nodes")
        tooltip_dict = {"nodes": self.node_hover, "edges": self.edge_hover}
        output_graph = self.strip_and_produce_rdf_graph(self.graph)
        p = hv.render(
            output_graph.options(
                frame_width=1000,
                frame_height=1000,
                xaxis=None,
                yaxis=None,
                tools=[tooltip_dict[tooltip]],
                inspection_policy=tooltip,
                node_color=self.node_color,
                edge_color=self.edge_color,
            ),
            backend="bokeh",
        )
        self.widget_output = jbk.BokehModel(p)
        self.children = [
            W.HTML("<h1>Visualization With Datashader"),
            self.widget_output,
        ]

    def strip_and_produce_rdf_graph(self, rdf_graph: Graph):
        sparql = self.sparql
        qres = rdf_graph.query(sparql)
        uri_graph = Graph()
        for row in qres:
            uri_graph.add(row)

        new_netx = rdflib_to_networkx_graph(uri_graph)
        original = hv.Graph.from_networkx(new_netx, self.layout,)
        output_graph = bundle_graph(original)
        return output_graph
