'''
Date: 2021.02.25 14:34:07
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2021.05.24 07:34:34
'''
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Tuple, Type, Union

from ._dag import DagEdge, DagNode, Edge, get_outgoing_edges

__all__ = [
    'Node',
    'NodeTypes',
    'Stream',
    'format_input_stream_tag',
    'get_filters_spec',
    'get_stream_spec_nodes',
    'streamable',
]


def get_stream_graph(stream_spec: Union[Stream, Dict[Any, Stream],
                                        List[Stream], Tuple[Stream]]) -> Dict[str, Stream]:
    stream_graph = dict()

    if isinstance(stream_spec, Dict):
        stream_graph = stream_spec
    elif isinstance(stream_spec, (List, Tuple)):
        stream_graph = dict(enumerate(stream_spec))
    elif isinstance(stream_spec, Stream):
        stream_graph = {None: stream_spec}

    return stream_graph


def get_stream_graph_nodes(stream_graph: Dict[str, Stream]) -> List[DagNode]:
    nodes = []

    for stream in stream_graph.values():
        if not isinstance(stream, Stream):
            raise TypeError(f"Expected <class 'Stream'>; got {type(stream)}")

        nodes.append(stream.Node)

    return nodes


def get_stream_spec_nodes(stream_spec: Any) -> List[DagNode]:
    return get_stream_graph_nodes(get_stream_graph(stream_spec))


def _get_types_repr(types: Tuple[Type]) -> str:
    if not isinstance(types, (List, Tuple)):
        types = [types]

    return ', '.join(['{}.{}'.format(x.__module__, x.__name__) for x in types])


class Stream(object):
    """Represents the outgoing edge of an upstream node;
    may be used to create more downstream nodes."""

    def __init__(self, upstream_node: DagNode, upstream_label: str, node_types=None, selector=None):
        if node_types and not isinstance(upstream_node, node_types):
            raise TypeError('Expected upstream node to be of one of the following type(s): '
                            '{}; got {}'.format(_get_types_repr(node_types), type(upstream_node)))

        self._node = upstream_node
        self._label = upstream_label
        self._selector = selector

    @property
    def Edge(self) -> Edge:
        return Edge(self.Node, self.Label, self.Selector)

    @property
    def Node(self):
        return self._node

    @property
    def Label(self):
        return self._label

    @property
    def Selector(self):
        return self._selector

    @property
    def audio(self) -> Stream:
        '''Select the audio-portion of a stream.'''
        return self['a']

    @property
    def video(self) -> Stream:
        '''Select the video-portion of a stream.'''
        return self['v']

    def view(self, save_path=None, detail=False, show_labels=True, pipe=False, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        node = self._node.__repr__()
        selector = f':{self._selector}' if self._selector else ''
        return f'{node}[{self.Label!r}{selector}]'

    def __getitem__(self, index: str) -> Stream:
        '''Select a component (audio, video) of the stream.'''
        if self._selector is not None:
            raise ValueError(f'Stream already has a selector: {self._selector}')
        elif not isinstance(index, str):
            raise TypeError(f"Expected string index (e.g. 'a'); got {index!r}")
        return self._node.stream(label=self._label, selector=index)


class NodeTypes(str, Enum):
    # https://stackoverflow.com/questions/58608361/string-based-enum-in-python

    Base = 'Base'
    Input = 'Input'
    Filter = 'Filter'
    Global = 'Global'
    Output = 'Output'

    # special filter nodes
    Movie = 'movie'


class Node(DagNode):

    def __init__(self, label: str, stream_spec, incoming_stream_types: Tuple[Type[Stream]],
                 outgoing_stream_type: Type[Stream], min_inputs=0, max_inputs=0,
                 node_type: str = NodeTypes.Base, args: List = None, kwargs: Dict = None):
        stream_graph = get_stream_graph(stream_spec)

        self._check_input_len(stream_graph, min_inputs, max_inputs)
        self._check_input_types(stream_graph, incoming_stream_types)

        incoming_edge_graph = self._get_incoming_edge_graph(stream_graph)

        super().__init__(label, incoming_edge_graph, node_type, args, kwargs)

        self._outgoing_stream_type = outgoing_stream_type
        self._incoming_stream_types = incoming_stream_types

    def stream(self, label: str = None, selector: str = None) -> Stream:
        """Create an outgoing stream originating from this node.

        More nodes may be attached onto the outgoing stream.
        """
        return self._outgoing_stream_type(self, label, selector=selector)

    def get_filter_spec(self, edges: Tuple[DagEdge] = None) -> str:
        if self.Type == NodeTypes.Filter:
            raise NotImplementedError

    def get_input_args(self) -> List[str]:
        if self.Type == NodeTypes.Input:
            raise NotImplementedError

    def get_output_args(self, stream_tag_graph: Dict[Tuple[DagNode, str], str]) -> List[str]:
        if self.Type == NodeTypes.Output:
            raise NotImplementedError

    def get_global_args(self) -> List[str]:
        if self.Type == NodeTypes.Global:
            raise NotImplementedError

    def __getitem__(self, index: Union[slice, str]) -> Stream:
        """Create an outgoing stream originating from this node; syntactic sugar for ``self.stream(label)``.
        It can also be used to apply a selector: e.g. ``node[0:'a']`` returns a stream with label 0 and
        selector ``'a'``, which is the same as ``node.stream(label=0, selector='a')``.

        Example:
            Process the audio and video portions of a stream independently::

                input = ffmpeg.input('audio_video.mp4')
                audio = input[:'a'].filter("aecho", 0.8, 0.9, 1000, 0.3)
                video = input[:'v'].hflip()
        """
        if isinstance(index, slice):
            return self.stream(label=index.start, selector=index.stop)
        else:
            return self.stream(label=index)

    @classmethod
    def _get_incoming_edge_graph(cls, stream_graph: Dict[str, Stream]) -> Dict[str, Edge]:
        incoming_edge_graph = {}
        for downstream_label, upstream in stream_graph.items():
            incoming_edge_graph[downstream_label] = upstream.Edge
        return incoming_edge_graph

    @classmethod
    def _check_input_len(cls, stream_graph, min_inputs: int, max_inputs: int):
        if min_inputs and len(stream_graph) < min_inputs:
            raise ValueError(f'Expected at least {min_inputs} input stream(s); got {len(stream_graph)}')
        elif max_inputs and min_inputs < max_inputs < len(stream_graph):
            raise ValueError(f'Expected at most {max_inputs} input stream(s); got {len(stream_graph)}')

    @classmethod
    def _check_input_types(cls, stream_graph, incoming_stream_types):
        for stream in stream_graph.values():
            if isinstance(stream, incoming_stream_types):
                continue
            raise TypeError('Expected incoming stream(s) to be of one of the following types:'
                            ' {}; got {}'.format(_get_types_repr(incoming_stream_types), type(stream)))


def streamable(stream: Stream = Stream):
    def wrapper(func):
        setattr(stream, func.__name__, func)
        return func

    return wrapper


def format_input_stream_tag(stream_tag_graph: Dict[Tuple[DagNode, str], str],
                            edge: DagEdge, is_final=False) -> str:
    prefix = stream_tag_graph[edge.UpstreamNode, edge.UpstreamLabel]
    suffix = f':{edge.Selector}' if edge.Selector else ''

    if is_final and edge.UpstreamNode.Type == NodeTypes.Input:
        _format = f'{prefix}{suffix}'  # Special case: `-map` args should not have brackets for input nodes.
    elif edge.DownstreamNode.Label == NodeTypes.Movie:
        _format = ''  # special filter
    elif edge.UpstreamNode.Label == NodeTypes.Movie:  # FIXME
        _format = f'[0][{prefix}{suffix}]'
    else:
        _format = f'[{prefix}{suffix}]'

    return _format


def format_output_stream_tag(stream_tag_graph: Dict[Tuple[DagNode, str], str], edge: DagEdge) -> str:
    return f'[{stream_tag_graph[edge.UpstreamNode, edge.UpstreamLabel]}]'


def get_filter_spec(node: Node, outgoing_edge_graph: Dict[str, List[Edge]],
                    stream_tag_graph: Dict[Tuple[DagNode, str], str]) -> str:
    incoming_edges = node.incoming_edges
    outgoing_edges = get_outgoing_edges(node, outgoing_edge_graph)

    inputs = [format_input_stream_tag(stream_tag_graph, edge) for edge in incoming_edges]
    outputs = [format_output_stream_tag(stream_tag_graph, edge) for edge in outgoing_edges]

    return f"{''.join(inputs)}{node.get_filter_spec(outgoing_edges)}{''.join(outputs)}"


def allocate_filter_stream_tags(filter_nodes: List[Node],
                                stream_tag_graph: Dict[Tuple[DagNode, str], str],
                                outgoing_edge_graphs: Dict[DagNode, Dict[str, List[Edge]]]):
    current_serial_number = 0

    for upstream_node in filter_nodes:
        outgoing_edge_graph = outgoing_edge_graphs[upstream_node]
        for upstream_label, downstreams in outgoing_edge_graph.items():
            if len(downstreams) > 1:
                raise ValueError(f"Encountered {upstream_node} with multiple outgoing edges "
                                 f"with same upstream label {upstream_label!r}; a `split` filter is probably required")

            stream_tag_graph[upstream_node, upstream_label] = f'tag{current_serial_number}'
            current_serial_number += 1


def get_filters_spec(filter_nodes: List[Node],
                     stream_tag_graph: Dict[Tuple[DagNode, str], str],
                     outgoing_edge_graphs: Dict[DagNode, Dict[str, List[Edge]]]) -> str:
    allocate_filter_stream_tags(filter_nodes, stream_tag_graph, outgoing_edge_graphs)
    return ';'.join(
            get_filter_spec(node, outgoing_edge_graphs[node], stream_tag_graph)
            for node in filter_nodes
    )
