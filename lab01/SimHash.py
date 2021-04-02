import hashlib
import sys

import numpy as np


def simhash(text, output_size=128):
    """
    Generates the hash (in bit array form) of a given text
    using the SimHash algorithm.

    :param text: the text to hash
    :param output_size: the size of the hash to generate
    :return: the hash of a given text in bit array form
    """
    terms = text.strip().split()
    sh = np.zeros(output_size, dtype=int)

    for term in terms:
        digest = hashlib.md5(term.encode()).digest()
        bits = np.unpackbits(np.frombuffer(digest, dtype=np.uint8))
        sh = (sh + 2 * bits) - 1

    return np.where(sh >= 0, 1, 0)


def hex_string(bit_array):
    """
    Converts the given bit array to a hex string.

    :param bit_array: the bit array to convert
    :return: the hex string representation of the given bit array
    """
    bit_string = ''.join(map(str, bit_array))

    return hex(int(bit_string, 2))[2:]


def sequential_search():
    """
    Performs a sequential search of similar texts based on
    user-specified queries.

    Similar files are identified based on the Hamming distance of
    their SimHash signatures.

    This function expects user input of the following format:
    * the first input contains the number of texts to read - N
    * the next N inputs are the N texts with space-separated tokens
    * the (N+1)-th input contains the number of queries to perform - Q
    * the next Q inputs are the Q queries of the form - I K
      * output the number of texts whose hashes differ from
        the hash of the I-th text by at most K bits
    """
    num_texts = int(next(sys.stdin).rstrip())
    text_hashes = [simhash(next(sys.stdin).rstrip()) for _ in range(num_texts)]

    num_queries = int(next(sys.stdin).rstrip())

    for _ in range(num_queries):
        i, k = map(int, next(sys.stdin).rstrip().split())
        ith_hash = text_hashes[i]

        num_diff_texts = -1  # excluding the i-th hash

        for text_hash in text_hashes:
            if (ith_hash != text_hash).sum() <= k:
                num_diff_texts += 1

        print(num_diff_texts)


if __name__ == '__main__':
    sequential_search()
