import numpy as np
from BaseMazeSolver import BaseMazeSolver
from Maze import BaseMazeCell
import random

class RecursiveCell(BaseMazeCell):
    def __init__(self, pos, parent):
        BaseMazeCell.__init__(self, pos)
        self.parent = parent
        self.children = self.connections.copy()
        if isinstance(self.parent, BaseMazeCell):
            self.children.remove(self.parent)

    @staticmethod
    def convert(base_cell, parent):
        base_cell.__class__ = RecursiveCell
        base_cell.parent = parent
        base_cell.children = base_cell.connections.copy()
        if isinstance(base_cell.parent, BaseMazeCell):
            base_cell.children.remove(base_cell.parent)
        return base_cell


class AnswerCell(BaseMazeCell):

    color = np.array([255, 255, 125])
    change_rate = 1

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.my_color = AnswerCell.color.copy()
        AnswerCell.updateColor()

    @classmethod
    def updateColor(cls):
        for i in range(1):
            i += 1
            if 125 <= cls.color[i] + cls.change_rate <= 255:
                cls.color[i] += cls.change_rate
            else:
                cls.change_rate *= -1


    def toImgArr(self, inner_size, border_size):
        size = inner_size + (border_size * 2)
        img = BaseMazeCell.toImgArr(self, inner_size, border_size)

        img[border_size : size - border_size, border_size : size - border_size, :] = np.ceil(self.my_color)

        for conn in [self.child, self.parent]:
            if isinstance(conn, BaseMazeCell):
                dir = tuple(conn.pos - self.pos)

                if dir == (0, 1):
                    img[border_size: size - border_size, size - border_size:, :] = np.ceil(self.my_color)

                if dir == (0, -1):
                    img[border_size: size - border_size, :border_size, :] = np.ceil(self.my_color)

                if dir == (1, 0):
                    img[size - border_size:, border_size: size - border_size, :] = np.ceil(self.my_color)

                if dir == (-1, 0):
                    img[:border_size, border_size: size - border_size, :] = np.ceil(self.my_color)


        return img.astype(np.uint8)


class FirstDepthSearchMazeSolver(BaseMazeSolver):
    def solve(self):
        self.maze.start = RecursiveCell.convert(self.maze.start, None)

        current_cell = self.maze.start

        while np.any(current_cell.pos != self.maze.end.pos):
            if len(current_cell.children) > 0:
                cell = random.choice(current_cell.children)
                cell = RecursiveCell.convert(cell, current_cell)
                current_cell.children.remove(cell)

                current_cell = cell

            else:
                current_cell = current_cell.parent

        child = None

        while current_cell is not None:
            parent = current_cell.parent

            current_cell.__class__ = AnswerCell
            current_cell.__init__(parent, child)

            child = current_cell
            current_cell = parent


