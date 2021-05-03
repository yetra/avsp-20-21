import sys
from collections import defaultdict


def parse_node_colors(num_nodes):
    """
    Parses node colors from sys.stdin.

    The function expects num_nodes lines where where line i contains 0 if
    the i-th node is white, and 1 if it is black.

    :param num_nodes: the number of nodes in the graph
    :return: a set of black node indices
    """
    black_nodes = set()

    for node in range(num_nodes):
        color = int(sys.stdin.readline().rstrip())

        if color == 1:
            black_nodes.add(node)

    return black_nodes


def parse_edges(num_edges):
    """
    Parses graph edges from sys.stdin.

    The function expects num_edges line where each line contains two node
    indices separated by a whitespace.

    :param num_edges: the number of edges in the graph
    :return: a dict representing the graph's adjacency matrix
    """
    adj_matrix = defaultdict(list)

    for _ in range(num_edges):
        node_1, node_2 = map(int, sys.stdin.readline().rstrip().split())

        adj_matrix[node_1].append(node_2)
        adj_matrix[node_2].append(node_1)

    return adj_matrix
