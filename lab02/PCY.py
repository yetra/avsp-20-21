import sys
from itertools import combinations
from collections import defaultdict


def print_output(item_counts, item_pairs, threshold):
    # number of frequent pairs - A-priori
    num_freq_items = sum(c for c in item_counts.values() if c >= threshold)
    print(num_freq_items * (num_freq_items - 1) / 2)

    # number of frequent pairs - PCY
    print(len(item_pairs))

    # frequent pair counts (descending)
    print(sorted(item_pairs.values(), reverse=True))


def pcy(num_baskets, num_buckets, threshold, basket_input):
    baskets = []

    # first pass
    item_counts = defaultdict(int)

    for basket_string in basket_input:
        basket = list(map(int, basket_string.rstrip().split()))
        baskets.append(basket)

        for item in basket:
            item_counts[item] += 1

    # second pass
    buckets = defaultdict(int)

    for basket in baskets:
        pairs = combinations(basket, 2)

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets
                buckets[k] += 1

    # third pass
    item_pairs = defaultdict(int)

    for basket in baskets:
        pairs = combinations(basket, 2)

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets

                if buckets[k] >= threshold:
                    item_pairs[i, j] += 1

    print_output(item_counts, item_pairs, threshold)


if __name__ == '__main__':
    num_baskets = int(sys.stdin.readline().rstrip())
    threshold = int(sys.stdin.readline().rstrip()) * num_baskets
    num_buckets = int(sys.stdin.readline().rstrip())

    pcy(num_baskets, num_buckets, threshold, sys.stdin)
