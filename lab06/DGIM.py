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

    def __str__(self):
        return f'Bucket(t={self.timestamp}, size={self.size})'


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

        if self.buckets and self._bucket_is_too_old():
            self.buckets.popleft()

        if bit == 0:
            return

        self.buckets.append(Bucket(self.timestamp, 1))
        self._merge_buckets()

    def count_ones(self, k):
        """
        Counts 1's in the last k bits of the stream.

        :param k: the number of last bits to check for 1's
        :return: the number of 1's in the last k bits
        """
        total_size = 0
        last_bucket_size = 0

        for i in range(len(self.buckets) - 1, -1, -1):
            if self.buckets[i].timestamp <= self.timestamp - k:
                break

            total_size += self.buckets[i].size
            last_bucket_size = self.buckets[i].size

        return total_size + int(last_bucket_size / 2)

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
            self.buckets[i - 1].size += self.buckets[i - 2].size
            self.buckets[i - 1].timestamp = self.buckets[i - 2].timestamp
            del self.buckets[i - 2]

            i = self._merge_index()


if __name__ == '__main__':
    window_size = int(sys.stdin.readline().rstrip())
    dgim = DGIM(window_size)

    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            break

        if line.startswith('q'):
            query_window_size = int(line[2:])
            print(dgim.count_ones(query_window_size))

        else:
            for bit in line:
                dgim.update(int(bit))
