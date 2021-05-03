import sys
from collections import defaultdict, deque


def closest_black_node(node, adj_matrix, black_nodes):
    """
    Finds the closest black node of a given node using BFS.

    :param node: the node whose closest black node needs to be found
    :param adj_matrix: the adjacency matrix in dict form
    :param black_nodes: a set of black node indices
    :return: the index of the closest black node and the corresponding distance
    """
    distance = 0

    visited = set()
    queue = deque()
    queue.append(node)

    while queue:
        curr_node = queue.pop()

        if curr_node in black_nodes:
            return curr_node, distance

        next_nodes = adj_matrix.get(node, [])

        for next_node in next_nodes:
            if next_node not in visited:
                visited.add(next_node)
                queue.append(next_node)

        distance += 1


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
    Parses graph edges from sys.stdin into an adjacency matrix.

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

    # sort the lists of adjacent nodes
    for adj_list in adj_matrix.values():
        adj_list.sort()

    return adj_matrix


if __name__ == '__main__':
    num_nodes, num_edges = map(int, sys.stdin.readline().rstrip().split())

    black_nodes = parse_node_colors(num_nodes)
    adj_matrix = parse_edges(num_edges)

    for node in range(num_nodes):
        closest, distance = closest_black_node(node, adj_matrix, black_nodes)
        print(f'{closest} {distance}')
