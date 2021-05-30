import sys
from collections import defaultdict
from collections.abc import MutableMapping

import numpy as np


class Graph:
    """Models a graph."""

    def __init__(self, edges, adj_matrix):
        """
        Initializes a Graph instance.

        :param edges: a dict of graph edges where the values represent weights
        :param adj_matrix: the adjacency matrix
        """
        self.edges = edges
        self.nodes = adj_matrix.keys()
        self.adj_matrix = adj_matrix

    def adjacent(self, node):
        """Returns nodes adjacent to the given node."""
        return self.adj_matrix[node]

    def remove_edge(self, edge):
        """Removes the given edge from the graph."""
        node_1, node_2 = edge
        self.edges.pop(edge)
        self.adj_matrix[node_1].remove(node_2)
        self.adj_matrix[node_2].remove(node_1)

    def communities(self):
        """Returns a generator of graph communities (connected node groups)."""
        seen = set()

        for node in self.nodes:
            if node not in seen:
                # BFS starting from node
                seen_from_node = set()
                queue = {node}

                while queue:
                    curr_queue, queue = queue, set()

                    for queued_node in curr_queue:
                        if queued_node not in seen_from_node:
                            seen_from_node.add(queued_node)
                            queue.update(self.adjacent(queued_node))

                seen.update(seen_from_node)
                yield seen_from_node

    @staticmethod
    def from_stdin():
        """Creates a Graph by reading edges and properties from sys.stdin."""
        edges, adj_matrix = Graph._parse_edges()
        properties = Graph._parse_properties()

        # update weights using node properties
        for node_1, node_2 in edges:
            max_similarity = len(properties[node_1])
            similarity = np.sum(properties[node_1] == properties[node_2])
            edges[node_1, node_2] = max_similarity - similarity + 1

        return Graph(edges, adj_matrix)

    @staticmethod
    def _parse_edges():
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

    @staticmethod
    def _parse_properties():
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

    @staticmethod
    def fromkeys(iterable, value=None):
        return UnorderedTupleKeyDict(dict.fromkeys(iterable, value))


def girvan_newmann(graph):
    """
    Implements the Girvan-Newmann algorithm.

    :param graph: the Graph instance
    :return: the best found communities based on modularity
    """
    best_modularity = None
    best_communities = None

    while graph.edges:
        edge_betweenness = calculate_betweenness(graph)

        max_betweenness = max(edge_betweenness.values())
        edges_to_remove = [list(e) for e, b in edge_betweenness.items()
                           if b == max_betweenness]

        # print sorted edges_to_remove
        edges_to_remove.sort(key=lambda e: (e[0], e[1]))
        for e in edges_to_remove:
            print(*e)

        for edge in edges_to_remove:
            graph.remove_edge(edge)

        if graph.edges:
            communities = tuple(graph.communities())
            modularity = calculate_modularity(communities, graph)

            if best_modularity is None or modularity > best_modularity:
                best_communities = communities
                best_modularity = modularity

    # print sorted best_communities
    sorted_best_communities = [sorted(c) for c in best_communities]
    sorted_best_communities.sort(key=lambda c: (len(c), c[0]))
    print(' '.join(map(lambda c: '-'.join(map(str, c)), sorted_best_communities)))

    return best_communities


def calculate_modularity(communities, graph):
    """
    Computes the modularity for the given communities.

    :param communities: the communities
    :param graph: the Graph instance
    """
    def ij_connected():
        """Returns True if the nodes i and j are in the same community."""
        for community in communities:
            if i not in community and j not in community:
                continue

            return i in community and j in community

    total = 0.0
    total_weight_doubled = sum(graph.edges.values()) * 2

    for i in graph.nodes:
        for j in graph.nodes:
            weight_ij = graph.edges.get((i, j), 0.0)
            weight_i = sum(graph.edges.get((i, k), 0.0) for k in graph.adjacent(i))
            weight_k = sum(graph.edges.get((j, k), 0.0) for k in graph.adjacent(j))

            total += ((weight_ij - (weight_i * weight_k) / total_weight_doubled)
                      * ij_connected())

    return total / total_weight_doubled


def calculate_betweenness(graph):
    """
    Calculates edge betweenness for the given graph.

    :param graph: the Graph instance
    :return: the edge betweenness dict
    """
    successors = floyd_warshall(graph)
    centralities = UnorderedTupleKeyDict.fromkeys(graph.edges, 0.0)

    for i in graph.nodes:
        for j in graph.nodes:
            paths = list(shortest_paths(successors, i, j))
            update_centralities(paths, centralities)

    for key, centrality in centralities.items():
        centralities[key] = centrality / 2.0

    return centralities


def floyd_warshall(graph):
    """
    Implements the Floyd-Warshall algorithm for weighted undirected graphs.
    This implementation keeps track of all shortest paths between node pairs.

    :param graph: the Graph instance
    :return: a dict of node successors for path reconstruction
    """
    costs = defaultdict(lambda: np.inf)
    successors = defaultdict(set)

    for (i, j), weight in graph.edges.items():
        costs[i, j] = costs[j, i] = weight
        successors[i, j].add(j)
        successors[j, i].add(i)

    for node in graph.nodes:
        costs[node, node] = 0

    for k in graph.nodes:
        for i in graph.nodes:
            cost_ik = costs[i, k]
            for j in graph.nodes:
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


if __name__ == '__main__':
    girvan_newmann(Graph.from_stdin())
