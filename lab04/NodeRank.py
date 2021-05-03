import sys

from scipy.sparse import csc_matrix


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


if __name__ == '__main__':
    num_nodes, beta = map(int, sys.stdin.readline().rstrip().split())
