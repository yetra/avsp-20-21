import numpy as np


def lsh(hashes, num_bands=8):
    candidates = dict.fromkeys(range(len(hashes)), set())

    for band in range(num_bands):
        buckets = {}

        for i, text_hash in enumerate(hashes):
            band_start, band_end = band * 16, (band + 1) * 16
            band_bits = text_hash[band_start:band_end]
            band_value = np.packbits(band_bits)

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
