class Bin:
    def __init__(self, capacity):
        self.capacity = capacity
        self.contents = 0

    def add_item(self, weight):
        self.contents += weight

    def get_contents(self):
        return self.contents
