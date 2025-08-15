import random
from constants import COLORS, SHAPES

class Piece:
    def __init__(self, x, y, shape=None):
        self.x = x
        self.y = y
        self.shape = shape if shape else random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.rotation = 0

def get_shape():
    return Piece(5, 0)
