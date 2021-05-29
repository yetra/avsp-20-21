import sys
from collections import defaultdict

import numpy as np


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


def add_weights(edges, properties):
    """
    Adds weights to the given edges dict using node properties.

    :param edges: dict of graph edges
    :param properties: dict of node property vectors
    :return: updated edges dict
    """
    max_similarity = len(properties.values()[0])

    for node_1, node_2 in edges:
        similarity = np.sum(properties[node_1] == properties[node_2])
        weight = max_similarity - similarity + 1

        edges[node_1, node_2] = weight

    return edges
