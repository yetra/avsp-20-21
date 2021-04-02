import sys
from collections import defaultdict


def pcy(num_baskets, num_buckets, threshold, basket_input):
    baskets = []

    # first pass
    item_counts = defaultdict(int)

    for basket_string in basket_input:
        basket = list(map(int, basket_string.rstrip().split()))
        baskets.append(basket)

        for item in basket:
            item_counts[item] += 1

    buckets = defaultdict(int)

    # second pass
    for basket in baskets:
        pairs = []

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets
                buckets[k] += 1

    # third pass
    item_pairs = defaultdict(int)

    for basket in baskets:
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
