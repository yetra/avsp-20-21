import sys


def parse_graph():
    """
    Parses input from sys.stdin into an adjacency matrix.

    The function expects input of the following form:
    * the first line contains the number of nodes and the beta probability
    * each row i of the following num_nodes rows contains the indices of nodes
      adjacent to i
    :return: the number of nodes in the graph, the beta probability value,
             and the parsed adjacency matrix
    """
    graph = {}

    num_nodes, beta = map(int, sys.stdin.readline().rstrip().split())

    for node in range(num_nodes):
        graph[node] = list(map(int, sys.stdin.readline().rstrip().split()))

    return num_nodes, beta, graph
