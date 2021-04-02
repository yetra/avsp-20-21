import sys


def pcy(num_baskets, num_buckets, threshold, basket_input):
    # first pass
    item_counts = {}
    for basket in basket_input:
        for item in basket:
            item_counts[item] += 1

    buckets = {}

    # second pass
    for basket in basket_input:
        pairs = []

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets
                buckets[k] += 1

    # third pass
    item_pairs = {}

    for basket in basket_input:
        pairs = []

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets

                if buckets[k] >= threshold:
                    item_pairs[i, j] += 1


if __name__ == '__main__':
    num_baskets = int(sys.stdin.readline().rstrip())
    threshold = int(sys.stdin.readline().rstrip()) * num_baskets
    num_buckets = int(sys.stdin.readline().rstrip())

    pcy(num_baskets, num_buckets, threshold, sys.stdin)
