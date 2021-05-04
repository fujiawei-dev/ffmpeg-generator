'''
Date: 2021.02-25 14:34:07
LastEditors: Rustle Karl
LastEditTime: 2021.04.25 14:03:16
'''
import tempfile

import graphviz

from ._dag import get_outgoing_edges, topological_sort
from ._node import get_stream_spec_nodes, Node, streamable
from .nodes import FilterNode, InputNode, OutputNode

__all__ = ['view']

_RIGHT_ARROW = '\u2192'


def _get_node_color(node: Node):
    color = None

    if isinstance(node, InputNode):
        color = '#99CC00'
    elif isinstance(node, OutputNode):
        color = '#99CCFF'
    elif isinstance(node, FilterNode):
        color = '#FFCC00'

    return color


@streamable()
def view(stream_spec, save_path=None, detail=False, show_labels=True, pipe=False):
    if pipe and save_path is not None:
        raise ValueError("Can\'t specify both `source` and `pipe`")
    elif not pipe and save_path is None:
        save_path = tempfile.mktemp()

    nodes = get_stream_spec_nodes(stream_spec)
    sorted_nodes, outgoing_edge_graphs = topological_sort(nodes)

    graph = graphviz.Digraph(format='png')
    graph.attr(rankdir='LR')

    for node in sorted_nodes:
        color = _get_node_color(node)

        if detail:
            label = node.detail
        else:
            label = node.brief

        graph.node(str(hash(node)), label, shape='box', style='filled', fillcolor=color)

        outgoing_edge_graph = outgoing_edge_graphs.get(node, {})
        for edge in get_outgoing_edges(node, outgoing_edge_graph):
            kwargs = {}
            upstream_label = edge.UpstreamLabel
            downstream_label = edge.DownstreamLabel
            selector = edge.Selector

            if show_labels and (upstream_label or downstream_label or selector):
                if upstream_label is None:
                    upstream_label = ''
                if selector is not None:
                    upstream_label += ":" + selector
                if downstream_label is None:
                    downstream_label = ''
                if upstream_label != '' and downstream_label != '':
                    middle = ' {} '.format(_RIGHT_ARROW)
                else:
                    middle = ''

                kwargs['label'] = '{}  {}  {}'.format(upstream_label, middle, downstream_label)

            upstream_node_id = str(hash(edge.UpstreamNode))
            downstream_node_id = str(hash(edge.DownstreamNode))

            graph.edge(upstream_node_id, downstream_node_id, **kwargs)

    if pipe:
        return graph.pipe()

    graph.view(save_path, cleanup=True)

    return stream_spec
