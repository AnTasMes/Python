import numpy as np


class BFS:
    def __init__(self, map, cover_map, row, col, put_char) -> None:
        self.visited = []
        self.map = map
        self.cover_map = cover_map
        self.row = row
        self.col = col
        self.put_char = put_char

        self.start_char = 0

    @staticmethod
    def get_neighbours(row, col, rows, cols, do_diagonals: bool = True):
        neighbours = []

        if row > 0:  # UP
            neighbours.append((row - 1, col))
        if row < rows - 1:  # DOWN
            neighbours.append((row + 1, col))
        if col > 0:  # LEFT
            neighbours.append((row, col - 1))
        if col < cols - 1:  # RIGHT
            neighbours.append((row, col + 1))

        if do_diagonals:
            if row > 0 and col > 0:
                neighbours.append((row - 1, col - 1))
            if row < rows - 1 and col < cols - 1:
                neighbours.append((row + 1, col + 1))
            if row < rows - 1 and col > 0:
                neighbours.append((row + 1, col - 1))
            if row > 0 and col < cols - 1:
                neighbours.append((row - 1, col + 1))

        return neighbours

    def uncover_bombs(self):
        for r_index, row in enumerate(self.map):
            for c_index, value in enumerate(row):
                if self.map[r_index][c_index] == -1:
                    self.cover_map[r_index][c_index] = -3
                else:
                    self.cover_map[r_index][c_index] = -1

        return self.cover_map

    def uncover_fields(self):

        def _search(row, col):
            if self.map[row][col] != 0:
                return
            self.visited.append((row, col))
            self.cover_map[row][col] = self.put_char

            coords = BFS.get_neighbours(
                row, col, self.map.shape[0], self.map.shape[1], do_diagonals=False)

            for r, c in coords:
                if (r, c) not in self.visited:
                    if self.map[r][c] == -1:
                        continue
                    if self.map[r][c] > 0:
                        self.cover_map[r][c] == -2
                    if self.map[r][c] == self.start_char:
                        _search(r, c)
                    self.visited.append((r, c))
                    self.cover_map[r][c] = self.put_char

        _search(self.row, self.col)
        return self.cover_map
