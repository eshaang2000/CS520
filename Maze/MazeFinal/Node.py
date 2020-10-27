import numpy as np
import random

class Node:

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0