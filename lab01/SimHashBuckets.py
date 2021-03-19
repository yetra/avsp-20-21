import numpy as np


def lsh(hashes, num_bands=8):
    powers_of_2 = 2 ** np.arange(16)[::-1]

    candidates = {i: set() for i in range(len(hashes))}

    for band in range(num_bands):
        buckets = {}

        for i, text_hash in enumerate(hashes):
            band_start, band_end = band * 16, (band + 1) * 16
            band_bits = text_hash[band_start:band_end]
            band_value = band_bits.dot(powers_of_2)

            if band_value in buckets:
                texts_in_bucket = buckets[band_value]

                for text_i in texts_in_bucket:
                    candidates[i].add(text_i)
                    candidates[text_i].add(i)

            else:
                texts_in_bucket = set()

            texts_in_bucket.add(i)
            buckets[band_value] = texts_in_bucket

    return candidates
