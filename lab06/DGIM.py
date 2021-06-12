import sys


class Bucket:
    """Models a bucket in the DGIM algorithm."""

    def __init__(self, timestamp, size):
        """
        Initializes a Bucket instance.

        :param timestamp: the timestamp at the creation of the bucket
        :param size: the size of the bucket (number of ones) - power of 2
        """
        self.timestamp = timestamp
        self.size = size


if __name__ == '__main__':
    window_size = int(sys.stdin.readline().rstrip())

    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            break

        if line.startswith('q'):
            # query
            query_window_size = int(line[2:])
            # TODO execute query

        else:
            # stream
            stream = map(int, line.split())
            # TODO handle stream
