import sys
from collections import defaultdict, MutableMapping

import numpy as np


class UnorderedTupleKeyDict(MutableMapping):
    """
    A dict of "unordered" tuple keys i.e. using the key (a, b) or (b, a)
    produces the same result.
    """

    def __init__(self, arg=None):
        self._map = {}
        if arg is not None:
            self.update(arg)

    def __getitem__(self, key):
        return self._map[frozenset(key)]

    def __setitem__(self, key, value):
        self._map[frozenset(key)] = value

    def __delitem__(self, key):
        del self._map[frozenset(key)]

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)


def girvan_newmann(edges, adj_matrix):
    """
    Implements the Girvan-Newmann algorithm.

    :param edges: dict of edge weights
    :param adj_matrix: adjacency matrix
    :return: the best found communities determined by modularity
    """
    best_modularity = None
    best_communities = None

    while edges:
        edge_betweenness = calculate_betweenness(edges, adj_matrix)

        max_betweenness = max(edge_betweenness.values())
        edges_to_remove = [e for e, b in edge_betweenness.items()
                           if b == max_betweenness]

        for node_1, node_2 in edges_to_remove:
            edges.pop((node_1, node_2))

            adj_matrix[node_1].remove(node_2)
            adj_matrix[node_2].remove(node_1)

        if edges:
            curr_communities = tuple(communities(adj_matrix))
            curr_modularity = modularity(curr_communities, edges, adj_matrix)

            if best_modularity is None or curr_modularity > best_modularity:
                best_communities = curr_communities
                best_modularity = curr_modularity

    return best_communities, best_modularity


def modularity(communities, edges, adj_matrix):
    """
    Computes the modularity for the given communities.

    :param communities: the communities
    :param edges: dict of edge weights
    :param adj_matrix: adjacency matrix
    :return: the computed modularity
    """
    def _connected(_i, _j, _communities):
        """Returns true if the given nodes are in the same community."""
        for _community in _communities:
            if _i not in _community and _j not in _community:
                continue

            return _i in _community and _j in _community

    total = 0.0
    total_weight_doubled = sum(edges.values()) * 2

    for i in adj_matrix.keys():
        for j in adj_matrix.keys():
            weight_ij = edges.get((i, j), 0.0)
            weight_i = sum(edges.get((i, k), 0.0) for k in adj_matrix[i])
            weight_k = sum(edges.get((j, k), 0.0) for k in adj_matrix[j])

            total += ((weight_ij - (weight_i * weight_k) / total_weight_doubled)
                      * _connected(i, j, communities))

    return total / total_weight_doubled


def communities(adj_matrix):
    """
    Finds communities (groups of connected nodes) in the given graph.

    :param adj_matrix: the adjacency matrix
    :return: communities generator
    """
    def _bfs(adj_matrix, source):
        """An implementation of BFS for finding connected nodes."""
        _seen = set()
        _queue = {source}

        while _queue:
            _current_nodes = _queue
            _queue = set()

            for _node in _current_nodes:
                if _node not in _seen:
                    _seen.add(_node)
                    _queue.update(adj_matrix[_node])

        return _seen

    seen = set()

    for node in adj_matrix.keys():
        if node not in seen:
            seen_from_node = _bfs(adj_matrix, node)
            seen.update(seen_from_node)
            yield seen_from_node


def calculate_betweenness(edges, adj_matrix):
    """
    Calculates edge betweenness for the given graph.

    :param edges: dict of edge weights
    :param adj_matrix: adjacency matrix
    :return: the edge betweenness dict
    """
    successors = floyd_warshall(edges, adj_matrix)
    centralities = dict.fromkeys(edges, 0.0)

    for i in adj_matrix.keys():
        for j in adj_matrix.keys():
            paths = list(shortest_paths(successors, i, j))
            update_centralities(paths, centralities)

    for key, centrality in centralities.items():
        centralities[key] = centrality / 2.0

    return centralities


def floyd_warshall(edges, adj_matrix):
    """
    Implements the Floyd-Warshall algorithm for weighted undirected graphs.
    This implementation keeps track of all shortest paths between node pairs.

    :param edges: dict of edge weights
    :param adj_matrix: adjacency matrix
    :return: a dict of node successors for path reconstruction
    """
    costs = defaultdict(lambda: np.inf)
    successors = defaultdict(set)

    for (i, j), weight in edges.items():
        costs[i, j] = costs[j, i] = weight
        successors[i, j].add(j)
        successors[j, i].add(i)

    for node in adj_matrix.keys():
        costs[node, node] = 0

    for k in adj_matrix.keys():
        for i in adj_matrix.keys():
            cost_ik = costs[i, k]
            for j in adj_matrix.keys():
                cost_ik_kj = cost_ik + costs[k, j]
                cost_ij = costs[i, j]

                if cost_ij > cost_ik_kj:
                    costs[i, j] = cost_ik_kj
                    successors[i, j] = set(successors[i, k])
                elif (cost_ij == cost_ik_kj and cost_ij != np.inf
                      and k != j and k != i):
                    successors[i, j].update(successors[i, k])

    return successors


def shortest_paths(successors, start_node, end_node):
    """
    Reconstructs all the shortest paths between the given nodes using a dict
    of successor nodes.

    :param successors: Floyd-Warshall dict of successor nodes obtained
    :param start_node: the first node of the shortest paths
    :param end_node: the last node of the shortest paths
    :return: a generator of shortest paths
    """
    if len(successors[start_node, end_node]) == 0:
        if start_node == end_node:
            yield [end_node]
        else:
            pass  # no path
    else:
        for k in successors[start_node, end_node]:
            for rest in shortest_paths(successors, k, end_node):
                yield [start_node] + rest


def update_centralities(paths, centralities):
    """
    Updates edge centralities for the given paths.

    :param paths: the shortest paths whose edges should be updated
    :param centralities: dict of edge centralities
    :return: the updated centralities dict
    """
    if len(paths) == 0:
        return

    centrality_coeff = 1.0 / len(paths)

    for path in paths:
        for i, j in zip(path[:-1], path[1:]):
            centralities[i, j] += centrality_coeff


def parse_edges():
    """
    Parses graph edges from sys.stdin.

    The function expects lines of two integers separated by a whitespace.
    The integers are indices of the nodes that the edge connects.

    :return: the parsed edges dict and adjacency matrix
    """
    edges = UnorderedTupleKeyDict()
    adj_matrix = defaultdict(list)

    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            break

        node_1, node_2 = map(int, line.split())

        edges[node_1, node_2] = 1
        adj_matrix[node_1].append(node_2)
        adj_matrix[node_2].append(node_1)

    return edges, adj_matrix


def parse_properties():
    """
    Parses node properties from sys.stdin.

    The function expects lines of integers separated by a whitespace.
    The first integer is the index of the node and the remaining integers
    are values of properties.

    :return: a dict of property vectors (numpy.ndarray)
    """
    properties = {}

    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            break

        line_parts = list(map(int, line.split()))
        node, properties_vector = line_parts[0], np.array(line_parts[1:])
        properties[node] = properties_vector

    return properties


def update_weights(edges, properties):
    """
    Updates edge weights using node properties.

    :param edges: dict of graph edges
    :param properties: dict of node property vectors
    """
    for node_1, node_2 in edges:
        max_similarity = len(properties[node_1])
        similarity = np.sum(properties[node_1] == properties[node_2])
        weight = max_similarity - similarity + 1

        edges[node_1, node_2] = weight
