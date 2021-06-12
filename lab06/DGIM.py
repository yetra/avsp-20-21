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

    def update(self, bit):
        """
        Updates the DGIM buckets with the given bit.

        :param bit: the bit to handle
        """
        self.timestamp += 1

        # delete oldest bucket if too old
        if self._bucket_is_too_old():
            self.buckets.popleft()

        # skip 0
        if bit == 0:
            return

        # add 1 to buckets
        self.buckets.append(Bucket(self.timestamp, 1))
        # and merge buckets while there are 3 of the same size
        self._merge_buckets()

    def _bucket_is_too_old(self):
        """Returns True if bucket is too old and should be removed."""
        return self.buckets[0].timestamp <= (self.timestamp - self.window_size)

    def _merge_index(self):
        """
        Returns the index of the newest such bucket if there are 3 buckets
        of the same size, else None.
        """
        if len(self.buckets) < 3:
            return

        for i in range(len(self.buckets) - 1, 1, -1):
            if (self.buckets[i].size
                    == self.buckets[i - 1].size
                    == self.buckets[i - 2].size):
                return i

        return

    def _merge_buckets(self):
        """Merges buckets if needed."""
        i = self._merge_index()

        while i is not None:
            # merge oldest two of the same size
            self.buckets[i - 1].size += self.buckets[i - 2]
            self.buckets[i - 1].timestamp = self.buckets[i - 2].timestamp
            del self.buckets[i - 2]

            i = self._merge_index()


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
