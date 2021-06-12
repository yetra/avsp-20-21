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
