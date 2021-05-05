import sys
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from scipy.sparse import csc_matrix


def node_rank(num_nodes, beta, M, max_iter, eps=1e-15):
    """
    Performs the NodeRank algorithm.

    :param num_nodes: the number of nodes in the graph
    :param beta: the probability of following a graph link
    :param M: the flow adjacency matrix (column-based)
    :param max_iter: the maximum number of algorithm iterations
    :param eps: stop the algorithm if difference between iteration results
                becomes <= eps
    :return: the rank vector
    """
    r = np.fill(num_nodes, 1. / num_nodes)
    teleport_probs = np.fill(num_nodes, (1 - beta) / num_nodes)

    for _ in range(max_iter):
        r_next = beta * M.multiply(r) + teleport_probs

        if np.abs(r_next - r) <= eps:
            return r_next

        r = r_next

    return r


def parse_M(num_nodes):
    """
    Constructs the M matrix used in NodeRank from sys.stdin input.

    The function expects num_nodes lines such that line i contains the indices
    of nodes adjacent to i.

    :return: the parsed M matrix in scipy.sparse.crc_matrix form
    """
    indptr = [0]
    indices = []
    data = []

    for node in range(num_nodes):
        adj_nodes = list(map(int, sys.stdin.readline().rstrip().split()))

        indices += adj_nodes
        data += [1. / len(adj_nodes)] * len(adj_nodes)
        indptr.append(len(indices))

    return csc_matrix((data, indices, indptr))


def handle_queries(num_nodes, beta, M):
    """
    Reads queries from sys.stdin and prints the required results.

    Each query consists of two integers separated by a whitespace:
    * node - the node whose rank should be calculated using NodeRank
    * max_iter - the maximum number of NodeRank iterations

    :param num_nodes: the number of nodes in the graph
    :param beta: the probability of following a graph link
    :param M: the flow adjacency matrix (column-based)
    """
    num_queries = int(sys.stdin.readline().rstrip())

    for _ in range(num_queries):
        node, max_iter = map(int, sys.stdin.readline().rstrip().split())
        r = node_rank(num_nodes, beta, M, max_iter)

        print(Decimal(Decimal(r[node]).quantize(
            Decimal('.0000000001'), rounding=ROUND_HALF_UP)))


if __name__ == '__main__':
    line_parts = sys.stdin.readline().rstrip().split()
    num_nodes, beta = int(line_parts[0]), float(line_parts[1])

    handle_queries(num_nodes, beta, parse_M(num_nodes))
