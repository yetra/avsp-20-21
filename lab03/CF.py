import sys

import numpy as np


def pearson_sim_matrix(x):
    """Calculates the Pearson similarity matrix for x."""
    return np.corrcoef(np.apply_along_axis(subtract_nonzero_mean, 1, x))


def subtract_nonzero_mean(x):
    """Subtracts the mean of nonzero elements from the nonzero elements in x."""
    return np.where(x > 0, x - x[x > 0].mean(), x)


def compute_rating(sims, ratings):
    """Returns the rating computed with the given similarities and ratings."""
    return (sims * ratings).sum() / sims.sum()


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
        k_most_similar_items = self._item_sims[item, :].argsort()[::-1][1:k+1]
        k_most_similar_item_ratings = self.ratings[k_most_similar_items, user]
        k_highest_sims = self._item_sims[item, k_most_similar_items]

        return compute_rating(k_highest_sims, k_most_similar_item_ratings)

    def _user_user(self, item, user, k):
        """
        Computes user-user CF rating for the specified item and user.

        :param item: the item whose rating will be computed
        :param user: the user whose item rating will be computed
        :param k: the number of most similar items to consider
        :return: the user-user CF rating
        """
        k_most_similar_users = self._user_sims[:, user].argsort()[::-1][1:k+1]
        k_most_similar_user_ratings = self.ratings[item, k_most_similar_users]
        k_highest_sims = self._user_sims[user, k_most_similar_users]

        return compute_rating(k_highest_sims, k_most_similar_user_ratings)

    def predict_rating(self, item, user, k, mode):
        """
        Predicts the rating of the specified item using item-item or
        user-user CF.

        :param item: the item whose rating will be predicted
        :param user: the user whose item rating will be predicted
        :param k: the k most similar users/items to consider
        :param mode: 0 for item-item CF, 1 for user-user CF
        :return: the predicted rating
        """
        if mode == 0:
            return self._item_item(item, user, k)
        elif mode == 0:
            return self._user_user(item, user, k)
        else:
            raise AttributeError(f'Unknown CF mode {mode}')


if __name__ == '__main__':
    num_items, num_users = map(int, sys.stdin.readline().rstrip().split())

    ratings = np.zeros((num_items, num_users))

    for item in range(num_items):
        item_ratings = sys.stdin.readline().rstrip().split()

        for user, rating in enumerate(item_ratings):
            if rating != 'X':
                ratings[item][user] = int(rating)
