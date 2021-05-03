import sys
from decimal import Decimal, ROUND_HALF_UP

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


def k_most_similar(idx, o_idx, k, sims, ratings):
    """Returns the k most similar indices (items or users)."""
    similar_idxs = sims[idx, :].argsort()[::-1]
    has_sim_gt_0 = sims[idx, similar_idxs] > 0
    has_rating = ratings[similar_idxs, o_idx] != 0
    k_most_similar_idxs = similar_idxs[has_sim_gt_0 & has_rating][:k]

    return k_most_similar_idxs


def predict_rating(idx, o_idx, k, sims, ratings):
    """Predicts the rating of a given item/user."""
    k_most_similar_idxs = k_most_similar(idx, o_idx, k, sims, ratings)
    k_most_similar_ratings = ratings[k_most_similar_idxs, o_idx]
    k_highest_sims = sims[idx, k_most_similar_idxs]

    return compute_rating(k_highest_sims, k_most_similar_ratings)


class CollaborativeFiltering:
    """Class for item-item and user-user collaborative filtering."""
    ITEM_ITEM_CF = 0
    USER_USER_CF = 1

    def __init__(self, ratings, num_items, num_users):
        """
        Inits the CollaborativeFiltering class.

        :param ratings: the num_items x num_users ratings matrix
        :param num_items: the total number of items
        :param num_users: the total number of users
        """
        self.ratings = ratings
        self.ratings_T = ratings.T

        self.num_items = num_items
        self.num_users = num_users

        self._item_sims = pearson_sim_matrix(ratings)
        self._user_sims = pearson_sim_matrix(self.ratings_T)

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
        if mode == self.ITEM_ITEM_CF:
            return predict_rating(item, user, k, self._item_sims, self.ratings)
        elif mode == self.USER_USER_CF:
            return predict_rating(user, item, k, self._user_sims, self.ratings_T)
        else:
            raise AttributeError(f'Unknown CF mode {mode}')


def parse_ratings():
    """
    Parses the ratings matrix from sys.stdin input.

    The following format is expected:
    * the first row is "num_items num_users"
    * the next num_items rows contain num_users integers specifying the ratings
      (or X if no rating is given for an item)
    :return: the ratings matrix, num_items, num_users
    """
    num_items, num_users = map(int, sys.stdin.readline().rstrip().split())

    ratings = np.zeros((num_items, num_users), dtype=int)

    for item in range(num_items):
        item_ratings = sys.stdin.readline().rstrip().split()

        for user, rating in enumerate(item_ratings):
            if rating != 'X':
                ratings[item][user] = int(rating)

    return ratings, num_items, num_users


def handle_queries(cf):
    """
    Reads and handles queries from sys.stdin.

    The following query format is expected: "I J T K"
    * I -- the item whose rating should be predicted
    * J -- the user whose item rating should be predicted
    * T -- the CF mode to use (0 = item-item, 1 = user-user)
    * K -- the number of most similar items/users to consider
    """
    num_queries = int(sys.stdin.readline().rstrip())

    for _ in range(num_queries):
        item, user, mode, k = map(int, sys.stdin.readline().rstrip().split())
        rating = cf.predict_rating(item - 1, user - 1, k, mode)

        print(Decimal(Decimal(rating).quantize(
            Decimal('.001'), rounding=ROUND_HALF_UP)))


if __name__ == '__main__':
    handle_queries(CollaborativeFiltering(*parse_ratings()))
