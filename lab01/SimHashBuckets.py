import sys

import numpy as np

from SimHash import simhash


def lsh(text_hashes, num_bands=8):
    """
    Finds candidates for text similarity using the LSH algorithm.

    :param text_hashes: the hashes of text documents to analyse
    :param num_bands: the number of bands for splitting the hashes
    :return: a dict of candidates for text similarity
             * key - index of text
             * value - set of indices of similarity candidates
    """
    band_size = len(text_hashes[0]) // num_bands
    powers_of_2 = 2 ** np.arange(band_size)[::-1]

    candidates = {i: set() for i in range(len(text_hashes))}

    for band in range(num_bands):
        buckets = {}

        for text_idx, text_hash in enumerate(text_hashes):
            start, end = band * band_size, (band + 1) * band_size
            band_value = text_hash[start:end].dot(powers_of_2)

            bucket = buckets.get(band_value, set())

            for idx in bucket:
                candidates[text_idx].add(idx)
                candidates[idx].add(text_idx)

            bucket.add(text_idx)
            buckets[band_value] = bucket

    return candidates


def lsh_search():
    """
    Performs a search of similar texts among LSH similarity candidates
    based on user-specified queries.

    Actually similar files among the LSH candidates are identified
    based on the Hamming distance of their SimHash signatures.

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

    candidates = lsh(text_hashes)

    num_queries = int(next(sys.stdin).rstrip())

    for _ in range(num_queries):
        i, k = map(int, next(sys.stdin).rstrip().split())
        ith_candidates = candidates.get(i, set())

        num_diff_texts = 0

        for text_idx in ith_candidates:
            if (text_hashes[i] != text_hashes[text_idx]).sum() <= k:
                num_diff_texts += 1

        print(num_diff_texts)


if __name__ == '__main__':
    lsh_search()
