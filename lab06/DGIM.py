import sys
from collections import deque


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


class DGIM:
    """
    An implementation of the Datar-Gionis-Indyk-Motwani (DGIM) algorithm
    for counting 1's.
    """

    def __init__(self, window_size):
        """
        Initializes a DGIM instance.

        :param window_size: size of the currently observable stream part
        """
        self.window_size = window_size

        self.timestamp = 0
        self.buckets = deque()

    def _bucket_is_too_old(self):
        """Returns True if bucket is too old and should be removed."""
        return self.buckets[0].timestamp <= (self.timestamp - self.window_size)


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
