class Node:

    def __init__(self, coord, g, f):
        self.coord = coord
        self.g = g
        self.f = f

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f
