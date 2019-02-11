from abc import abstractmethod
import numpy as np

class BaseMazeGenerator:
    def __init__(self, maze):
        self.maze = maze

    @abstractmethod
    def generate(self):
        pass

