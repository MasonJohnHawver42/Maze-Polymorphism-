from Maze import *
from BaseMazeCreator import *


class HuntandKillCell(BaseMazeCell):
    """ The purpose is to add parent and child fields, for recursive purposes."""
    def __init__(self, pos, parent):
        BaseMazeCell.__init__(self, pos)
        self.parent = parent
        if isinstance(self.parent, HuntandKillCell):
            self.connections.append(parent)


class HuntandKillMazeGenerator(BaseMazeGenerator):

    def getNeighboursPos(self, cell):
        directions = np.array([[0, -1], [1, 0], [0, 1], [-1, 0]])
        positions = np.tile(cell.pos, directions.shape[0]).reshape((4, 2))
        new_pos = positions + directions

        valid_pos = ((new_pos >= 0) * (new_pos < np.asarray(self.maze.size)))
        mask = np.all(valid_pos, 1).repeat(2)
        mask = mask.reshape(int(mask.shape[0] / 2), 2)

        new_pos = new_pos[mask]
        new_pos = new_pos.reshape(int(new_pos.shape[0]/2), 2)
        return new_pos

    def getEmptyNeighboursPos(self, cell):
        pos = self.getNeighboursPos(cell)
        neighbours = self.maze.cells[pos[:, 0], pos[:, 1]].reshape((pos.shape[0], 1))

        mask = (neighbours == None).repeat(2)
        mask = mask.reshape((int(mask.shape[0]/2), 2))

        empty_n = pos[mask]
        return empty_n.reshape((int(empty_n.shape[0]/ 2), 2))

    def getRandomNeighborPos(self, cell, neighbor_pos, horizontal_bias=.5, vertical_bias=.5):
        if horizontal_bias == .5 and vertical_bias == .5:
            return neighbor_pos[np.random.randint(neighbor_pos.shape[0])]
        else:
            bias = neighbor_pos - cell.pos
            bias = (np.all(bias == np.array([0, 1]), 1)) + (np.all(bias == np.array([0, -1]), 1))
            if np.sum(bias) == 0 or np.sum(bias) == bias.shape[0]:
                bias = np.ones(bias.shape[0]) / bias.shape[0]
            else:
                bias = bias.astype(np.float64) * np.nan_to_num(horizontal_bias / np.sum(bias))
                bias += (bias == 0) * np.nan_to_num(vertical_bias / sum(bias == 0))

            return neighbor_pos[np.random.choice(np.arange(neighbor_pos.shape[0]), 1, p=bias)][0]

    def generate(self):

        head = HuntandKillCell((0, 0), None)

        current_cell = head

        i = 0
        while current_cell is not None:
            neighbors = self.getEmptyNeighboursPos(current_cell)
            if neighbors.shape[0] > 0:
                new_pos = self.getRandomNeighborPos(current_cell, neighbors)

                new_cell = HuntandKillCell(new_pos, current_cell)
                current_cell.addConnection(new_cell)
                self.maze.cells[new_pos[0], new_pos[1]] = new_cell

                current_cell = new_cell
                i += 1

            else:
                current_cell = current_cell.parent

        self.maze.start = self.maze.cells[0, 0]
        self.maze.end = self.maze.cells[self.maze.size[0] - 1, self.maze.size[1] - 1]
