from bin import Bin


class Warehouse:
    def __init__(self):
        self.bins = []

    def add_bin(self, capacity):
        new_bin = Bin(capacity)
        self.bins.append(new_bin)
        return new_bin

    def get_bins(self):
        return self.bins

