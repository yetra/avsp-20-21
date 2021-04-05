import sys
from itertools import combinations
from collections import defaultdict


def print_output(item_counts, freq_pairs, threshold):
    """Prints the PCY algorithm output."""
    # number of frequent pairs - A-priori
    num_freq_items = sum(c >= threshold for c in item_counts.values())
    print(num_freq_items * (num_freq_items - 1) // 2)

    # number of frequent pairs - PCY
    print(len(freq_pairs))

    # frequent pair counts (descending)
    sorted_pair_counts = sorted(freq_pairs.values(), reverse=True)

    for count in sorted_pair_counts:
        if count >= threshold:
            print(count)


def pcy(num_baskets, num_buckets, threshold, basket_input):
    """
    Performs the PCY algorithm and prints the results.

    :param num_baskets: the number of baskets containing items
    :param num_buckets: the number of buckets to create
    :param threshold: the threshold to cross to be considered frequent
    :param basket_input: a file-like object where each basket is in its own
                         line and items are separated by a single space
    """
    baskets = []

    # first pass - count individual items
    item_counts = defaultdict(int)

    for basket_string in basket_input:
        basket = list(map(int, basket_string.rstrip().split()))
        baskets.append(basket)

        for item in basket:
            item_counts[item] += 1

    # second pass - hash each item pair into a bucket and increase its count
    buckets = defaultdict(int)

    for basket in baskets:
        pairs = combinations(basket, 2)

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets
                buckets[k] += 1

    # third pass - count frequent item pairs
    freq_pairs = defaultdict(int)

    for basket in baskets:
        pairs = combinations(basket, 2)

        for i, j in pairs:
            if item_counts[i] >= threshold and item_counts[j] >= threshold:
                k = ((i * len(item_counts)) + j) % num_buckets

                if buckets[k] >= threshold:
                    freq_pairs[i, j] += 1

    print_output(item_counts, freq_pairs, threshold)


if __name__ == '__main__':
    num_baskets = int(sys.stdin.readline().rstrip())
    threshold = float(sys.stdin.readline().rstrip()) * num_baskets
    num_buckets = int(sys.stdin.readline().rstrip())

    pcy(num_baskets, num_buckets, threshold, sys.stdin)
