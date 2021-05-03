import sys


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
