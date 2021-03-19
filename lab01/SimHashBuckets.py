import numpy as np


def lsh(text_hashes, num_bands=8):
    band_size = len(text_hashes[0]) / num_bands
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
