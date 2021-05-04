'''
Date: 2021.02.26 21:39:59
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.04.29 15:42:51
'''
from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from typing import Dict, List, NamedTuple, Tuple

__all__ = [
    "DagEdge",
    "DagNode",
    "Edge",
    "get_incoming_edges",
    "get_outgoing_edges",
    "topological_sort"
]


class Edge(NamedTuple):
    Node: DagNode
    Label: str
    Selector: str


class DagEdge(NamedTuple):
    '''DagNodes are connected by edges. An edge
    connects two nodes with a label for each side.'''

    DownstreamNode: DagNode  # downstream/child node
    DownstreamLabel: str  # label on the incoming side of the downstream node
    UpstreamNode: DagNode  # upstream/parent node
    UpstreamLabel: str  # label on the outgoing side of the upstream node
    Selector: str


class DagNode(object):
    '''Node in a directed-acyclic graph (DAG).'''

    def __init__(self, label: str, incoming_edge_graph: Dict[str, Edge],
                 node_type: str, args: List, kwargs: Dict):
        self._label = label
        self._args = list(map(str, args)) if args else []
        self._kwargs = kwargs or {}
        self._node_type = node_type
        self._incoming_edge_graph = incoming_edge_graph

    def __repr__(self):
        return f"<class 'DagNode:{self.Type}'> {self.detail}"

    @cached_property
    def detail(self) -> str:
        """Return a full string representation of the node."""
        props = self._args + [f'{k}={self._kwargs[k]}' for k in sorted(self._kwargs)]
        if props:
            return f'{self.brief}:{",".join(props)}'
        else:
            return self.brief

    @property
    def brief(self) -> str:
        """Return a partial/concise representation of the node."""
        return self._label

    @property
    def Label(self) -> str:
        return self._label

    @property
    def Type(self) -> str:
        return self._node_type

    @property
    def incoming_edge_graph(self) -> Dict[str, Edge]:
        return self._incoming_edge_graph

    @cached_property
    def incoming_edges(self) -> Tuple[DagEdge]:
        """Provides information about all incoming edges that connect to this node."""
        return get_incoming_edges(self, self.incoming_edge_graph)

    def stream(self, label: str = None, selector: str = None) -> DagEdge:
        raise NotImplementedError

    # TODO cause recursion, maybe it's not a good idea. It doesn't seem necessary.
    # def __eq__(self, other: DagNode):
    #     return (self.Type, self.detail, self.incoming_edges) == (other.Type, other.detail, other.incoming_edges)
    #
    # def __hash__(self):
    #     return hash((self.Type, self.detail))


def get_incoming_edges(node: DagNode, incoming_edge_graph: Dict[str, Edge]) -> Tuple[DagEdge]:
    incoming_edges = []
    for label, edge in incoming_edge_graph.items():
        incoming_edges.append(DagEdge(node, label, edge.Node, edge.Label, edge.Selector))
    return tuple(incoming_edges)


def get_outgoing_edges(node: DagNode, outgoing_edge_graph: Dict[str, List[Edge]]) -> Tuple[DagEdge]:
    outgoing_edges = []
    for label, edges in outgoing_edge_graph.items():
        for edge in edges:
            outgoing_edges.append(DagEdge(edge.Node, edge.Label, node, label, edge.Selector))
    return tuple(outgoing_edges)


def topological_sort(nodes: List[DagNode]) -> Tuple[Tuple[DagNode], Dict[DagNode, Dict[str, List[Edge]]]]:
    '''NOTE nodes can be part of the nodes, but not all.

    DagNodes may have any number of incoming edges and any number of
    outgoing edges.  DagNodes keep track only of their incoming edges, but
    the entire graph structure can be inferred by looking at the furthest
    downstream nodes and working backwards.
    '''
    outgoing_edge_graphs = defaultdict(lambda: defaultdict(list))
    dependent_count = defaultdict(lambda: 0)
    outgoing_graph = defaultdict(list)
    visited_nodes = set()
    sorted_nodes = []

    # Convert to a friendly representation
    while nodes:
        node = nodes.pop()
        if node not in visited_nodes:
            for edge in node.incoming_edges:
                outgoing_graph[edge.UpstreamNode].append(node)  # node == edge.DownstreamNode
                outgoing_edge_graphs[edge.UpstreamNode][edge.UpstreamLabel]. \
                    append(Edge(node, edge.DownstreamLabel, edge.Selector))
                nodes.append(edge.UpstreamNode)
            visited_nodes.add(node)

    # Calculate the number of dependents
    for val in outgoing_graph.values():
        for v in val:
            dependent_count[v] += 1

    # Zero dependent nodes
    stack = [node for node in visited_nodes if dependent_count[node] == 0]

    while stack:
        node = stack.pop()
        sorted_nodes.append(node)

        for n in outgoing_graph[node]:
            dependent_count[n] -= 1
            if dependent_count[n] == 0:
                stack.append(n)

    if len(sorted_nodes) != len(visited_nodes):
        raise RuntimeError('This graph is not a DAG')

    return tuple(sorted_nodes), outgoing_edge_graphs
