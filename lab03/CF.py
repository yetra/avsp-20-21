import sys

if __name__ == '__main__':
    num_items, num_users = map(int, sys.stdin.readline().rstrip().split())

    ratings = {}

    for item in range(num_items):
        line_parts = sys.stdin.readline().rstrip().split()
        item_ratings = map(lambda x: 0 if x == 'X' else int(x), line_parts)

        for user, rating in enumerate(item_ratings):
            ratings[item, user] = rating
