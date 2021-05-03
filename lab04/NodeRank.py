import sys
from scipy.sparse import csr_matrix


def parse_graph(num_nodes):
    """
    Parses input from sys.stdin into a sparse adjacency matrix.

    The function expects num_nodes lines such that line i contains the indices
    of nodes adjacent to i.

    :return: the parsed adjacency matrix in scipy.sparse.crs_matrix form
    """
    indptr = [0]
    indices = []
    data = []

    for node in range(num_nodes):
        adj_nodes = list(map(int, sys.stdin.readline().rstrip().split()))

        indices += adj_nodes
        data += [1] * len(adj_nodes)
        indptr.append(len(indices))

    return csr_matrix((data, indices, indptr), dtype=int)


if __name__ == '__main__':
    num_nodes, beta = map(int, sys.stdin.readline().rstrip().split())
