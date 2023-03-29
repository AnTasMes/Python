import numpy as np
from floodfill import floodFill

rowCount = 5
columCount = 5
maxBombs = 4


def PrintMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def MakeMap(W, H, maxBombs):
    mat = [['+' for x in range(columCount)]
           for y in range(rowCount)]

    while maxBombs > 0:
        x = np.random.randint(0, rowCount-1)
        y = np.random.randint(0, columCount-1)
        if not mat[x][y] == 'B':
            mat[x][y] = 'B'
            maxBombs -= 1
    return mat


def RandomMap(W, H):
    mat = [[np.random.randint(0, 2) for x in range(columCount)]
           for y in range(rowCount)]
    for i, row in enumerate(mat):
        for j, elem in enumerate(row):
            if mat[i][j] == 1:
                mat[i][j] = 'B'
            else:
                mat[i][j] = '+'
    return mat


def GoThroughMap(matrix):
    temp = matrix
    for rowIndex, row in enumerate(temp):
        for columIndex, elem in enumerate(row):
            b_count = 0
            if temp[rowIndex][columIndex] == 'B':
                continue
            try:
                if temp[rowIndex+1][columIndex] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex-1][columIndex] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex][columIndex+1] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex][columIndex-1] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex-1][columIndex-1] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex+1][columIndex+1] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex-1][columIndex+1] == 'B':
                    b_count += 1
            except:
                pass
            try:
                if temp[rowIndex+1][columIndex-1] == 'B':
                    b_count += 1
            except:
                pass
            if b_count > 0:
                temp[rowIndex][columIndex] = b_count
    return temp


if __name__ == '__main__':
    bombField = MakeMap(rowCount, columCount, maxBombs)
    PrintMatrix(bombField)
    tempBf = bombField
    print()
    GoThroughMap(tempBf)
    PrintMatrix(bombField)
    # PrintMatrix(bombField)
