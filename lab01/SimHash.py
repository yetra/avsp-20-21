import hashlib

import numpy as np


def simhash(text, output_size=128):
    """
    Generates the hash (in bit array form) of a given text using the SimHash algorithm.

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
    """Converts the given bit array to a hex string."""
    bit_string = ''.join(map(str, bit_array))

    return hex(int(bit_string, 2))[2:]


if __name__ == '__main__':
    print(simhash('fakultet elektrotehnike i racunarstva'))
