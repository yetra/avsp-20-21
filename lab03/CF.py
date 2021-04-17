import sys

import numpy as np


def pearson_sim_matrix(x):
    """Calculates the Pearson similarity matrix for x."""
    return np.corrcoef(np.apply_along_axis(subtract_nonzero_mean, 1, x))


def subtract_nonzero_mean(x):
    """Subtracts the mean of nonzero elements from the nonzero elements in x."""
    return np.where(x > 0, x - x[x > 0].mean(), x)


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

        self._item_sims = pearson_sim_matrix(ratings)
        self._user_sims = pearson_sim_matrix(ratings.T)

    def _item_item(self, item, user, k):
        """
        Computes item-item CF rating for the specified item and user.

        :param item: the item whose rating will be computed
        :param user: the user whose item rating will be computed
        :param k: the number of most similar items to consider
        :return: the item-item CF rating
        """
        k_most_similar_items = self._item_sims[item, :].argsort()[::-1][:k]
        k_most_similar_item_ratings = self.ratings[k_most_similar_items, user]
        k_highest_sims = self._item_sims[item, k_most_similar_items]

        return ((k_highest_sims * k_most_similar_item_ratings).sum()
                / k_highest_sims.sum())

    def _user_user(self, item, user, k):
        """
        Computes user-user CF rating for the specified item and user.

        :param item: the item whose rating will be computed
        :param user: the user whose item rating will be computed
        :param k: the number of most similar items to consider
        :return: the user-user CF rating
        """
        k_most_similar_users = self._user_sims[:, user].argsort()[::-1][:k]
        k_most_similar_user_ratings = self.ratings[item, k_most_similar_users]
        k_highest_sims = self._user_sims[user, k_most_similar_users]

        return ((k_highest_sims * k_most_similar_user_ratings).sum()
                / k_highest_sims.sum())


if __name__ == '__main__':
    num_items, num_users = map(int, sys.stdin.readline().rstrip().split())

    ratings = np.zeros((num_items, num_users))

    for item in range(num_items):
        item_ratings = sys.stdin.readline().rstrip().split()

        for user, rating in enumerate(item_ratings):
            if rating != 'X':
                ratings[item][user] = int(rating)
