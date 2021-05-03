import sys
from scipy.sparse import csr_matrix


def parse_graph():
    """
    Parses input from sys.stdin into a sparse adjacency matrix.

    The function expects input of the following form:
    * the first line contains the number of nodes and the beta probability
    * each row i of the following num_nodes rows contains the indices of nodes
      adjacent to i
    :return: the number of nodes in the graph, the beta probability value,
             and the parsed adjacency matrix in scipy.sparse.crs_matrix form
    """
    num_nodes, beta = map(int, sys.stdin.readline().rstrip().split())

    indptr = [0]
    indices = []
    data = []

    for node in range(num_nodes):
        adj_nodes = list(map(int, sys.stdin.readline().rstrip().split()))

        indices += adj_nodes
        data += [1] * len(adj_nodes)
        indptr.append(len(indices))

    adj_matrix = csr_matrix((data, indices, indptr), dtype=int)

    return num_nodes, beta, adj_matrix
