import sys
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from scipy.sparse import csc_matrix


class NodeRank:
    """The NodeRank algorithm class."""

    def __init__(self, num_nodes, beta, M, eps=1e-15):
        """
        Initializes the NodeRank class.

        :param num_nodes: the number of nodes in the graph
        :param beta: the probability of following a graph link
        :param M: the flow adjacency matrix (column-based)
        :param eps: stop the algorithm if difference between iteration results
                    becomes <= eps
        """
        self.num_nodes = num_nodes
        self.beta = beta
        self.M = M
        self.eps = eps

        self.r_stored = [np.array([1. / num_nodes] * num_nodes)]
        self.teleport_probs = np.array([(1 - beta) / num_nodes] * num_nodes)

    def run(self, max_iter):
        """
        Runs the NodeRank algorithm.

        Precomputed rank vectors are stored in a list for faster execution.

        :param max_iter: the maximum number of algorithm iterations
        :return: the rank vector
        """
        if max_iter <= len(self.r_stored) - 1:
            return self.r_stored[max_iter]

        r = self.r_stored[-1]

        for _ in range(len(self.r_stored) - 1, max_iter):
            r_next = beta * (self.M @ r) + self.teleport_probs
            self.r_stored.append(r_next)

            if np.abs(r_next - r).sum() <= self.eps:
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

    return csc_matrix((data, indices, indptr), shape=(num_nodes, num_nodes))


def handle_queries(node_rank):
    """
    Reads queries from sys.stdin and prints the required results.

    Each query consists of two integers separated by a whitespace:
    * node - the node whose rank should be calculated using NodeRank
    * max_iter - the maximum number of NodeRank iterations

    :param node_rank: the NodeRank instance to use
    """
    num_queries = int(sys.stdin.readline().rstrip())

    for _ in range(num_queries):
        node, max_iter = map(int, sys.stdin.readline().rstrip().split())
        r = node_rank.run(max_iter)

        print(Decimal(Decimal(r[node]).quantize(
            Decimal('.0000000001'), rounding=ROUND_HALF_UP)))


if __name__ == '__main__':
    line_parts = sys.stdin.readline().rstrip().split()
    num_nodes, beta = int(line_parts[0]), float(line_parts[1])
    node_rank = NodeRank(num_nodes, beta, parse_M(num_nodes))

    handle_queries(node_rank)
