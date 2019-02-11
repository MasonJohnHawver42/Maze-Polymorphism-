
import inspect
from BaseMazeCreator import *
from BaseMazeSolver import *
import numpy as np
import cv2

class BaseMazeCell:
    def __init__(self, pos):
        self.pos = np.asarray(pos)
        self.connections = []

    def addConnection(self, connection):
        if isinstance(connection, BaseMazeCell):
            self.connections.append(connection)

    def toImgArr(self, inner_size, border_size):

        size = inner_size + (border_size * 2)

        img = np.zeros((size, size, 3))
        img[border_size: size - border_size, border_size: size - border_size, :] = 255

        for conn in self.connections:
            dir = tuple(conn.pos - self.pos)

            if dir == (0, 1):
                img[border_size: size - border_size, size - border_size:, :] = 255

            if dir == (0, -1):
                img[border_size: size - border_size, :border_size, :] = 255

            if dir == (1, 0):
                img[size - border_size:, border_size: size - border_size, :] = 255

            if dir == (-1, 0):
                img[:border_size, border_size: size - border_size, :] = 255

        return img.astype(np.uint8)

    def showCell(self, inner_size, border_size):
        img = self.toImgArr(inner_size, border_size)
        cv2.imshow("", img)
        cv2.waitKey(0)

    def __repr__(self):
        return np.array2string(np.asarray(self.pos))



class Maze(object):
    def __init__(self, size):
        self.size = size
        self.cells = np.empty(self.size, dtype=object)

        self.start = self.cells[0, 0]
        self.end = self.cells[self.size[0] - 1, self.size[1] - 1]

    def addSilhouette(self, silhouette):
        sil = cv2.imread("silhouette.jpg")
        sil = (sil[:, :, 0] < 200)


    def generateMaze(self, mazeGenerator):
        if inspect.isclass(mazeGenerator):
            if issubclass(mazeGenerator, BaseMazeGenerator):
                mazeGenerator(self).generate()
        elif isinstance(mazeGenerator, BaseMazeGenerator):
            mazeGenerator.generate()

    def findSolution(self, mazeSolver):
        if inspect.isclass(mazeSolver):
            if issubclass(mazeSolver, BaseMazeSolver):
                mazeSolver(self).solve()
        elif isinstance(mazeSolver, BaseMazeSolver):
            mazeSolver.solve()

    def toImgArr(self, inner_size, border_size):
        size = inner_size + (border_size * 2)
        img_size = np.asarray(self.cells.shape[0: 2]) * size
        img = np.zeros((img_size[0], img_size[1], 3))

        for row in range(self.cells.shape[0]):
            for col in range(self.cells.shape[1]):
                if isinstance(self.cells[row, col], BaseMazeCell):
                    img[row * size: (row + 1) * size, col * size: (col + 1) * size, :] = self.cells[row, col].toImgArr(inner_size, border_size)

        img[(self.start.pos[0] * size) + border_size: ((self.start.pos[0] + 1) * size) - border_size, (self.start.pos[1] * size) + border_size: ((self.start.pos[1] + 1) * size) - border_size, :] = np.array([0, 255, 0])
        img[(self.end.pos[0] * size) + border_size: ((self.end.pos[0] + 1) * size) - border_size, (self.end.pos[1] * size) + border_size: ((self.end.pos[1] + 1) * size) - border_size, :] = np.array([0, 0, 255])

        return img.astype(np.uint8)

    def showMaze(self, inner_size, border_size):
        img = self.toImgArr(inner_size, border_size)
        cv2.imshow("", img)
        cv2.waitKey(0)

