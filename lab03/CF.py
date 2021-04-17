import sys

import numpy as np


class CollaborativeFiltering:
    """Class for item-item and user-user collaborative filtering."""

    def __init__(self, ratings, num_items, num_users):
        """
        Inits the CollaborativeFiltering class.

        :param ratings: the num_items x num_users ratings matrix
        :param num_items: the total number of items
        :param num_users: the total number of users
        """
        self.ratings = ratings

        self.num_items = num_items
        self.num_users = num_users


if __name__ == '__main__':
    num_items, num_users = map(int, sys.stdin.readline().rstrip().split())

    ratings = np.zeros((num_items, num_users))

    for item in range(num_items):
        item_ratings = sys.stdin.readline().rstrip().split()

        for user, rating in enumerate(item_ratings):
            if rating != 'X':
                ratings[item][user] = int(rating)
