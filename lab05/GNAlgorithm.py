import sys
from collections import defaultdict


def parse_edges():
    """
    Parses graph edges from sys.stdin.

    The function expects lines of two integers separated by a whitespace.
    The integers are indices of the nodes that the edge connects.

    :return: the parsed edges dict and adjacency matrix
    """
    edges = {}
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
