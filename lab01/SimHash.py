import hashlib

import numpy as np


def simhash(text, output_size=128):
    """
    Generates the hash of a given text using the SimHash algorithm.

    :param text: the text to hash
    :param output_size: the size of the hash to generate
    :return: the hash of a given text
    """
    terms = text.strip().split()
    sh = np.zeros(output_size, dtype=int)

    for term in terms:
        digest = hashlib.md5(term.encode()).hexdigest()
        bitstring = bin(int(digest, 16))[2:].zfill(output_size)
        bits = np.array(list(bitstring), dtype=int)
        sh += 2 * bits - 1

    output = ''.join('1' if x >= 0 else '0' for x in sh)

    return hex(int(output, 2))


if __name__ == '__main__':
    print(simhash('fakultet elektrotehnike i racunarstva'))
