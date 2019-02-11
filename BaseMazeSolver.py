from abc import abstractmethod
import numpy as np

class BaseMazeSolver:
    def __init__(self, maze):
        self.maze = maze

    @abstractmethod
    def solve(self):
        pass

