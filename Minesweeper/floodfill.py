from numpy.core.records import array


def printMatrix(matrix):
    for row in matrix:
        print(row)
    print()


def floodFill(matrix: list[list[str]], row: int, column: int):
    base = matrix[row][column]
    matrix[row][column] = 'x'
    # Go up
    try:
        if matrix[row-1][column] == base and row-1 >= 0:
            printMatrix(matrix)
            matrix = floodFill(matrix, row-1, column)
    except:
        pass
    # Go right
    try:
        if matrix[row][column+1] == base:
            printMatrix(matrix)
            matrix = floodFill(matrix, row, column+1)
    except:
        pass
    # Go down
    try:
        if matrix[row+1][column] == base:
            printMatrix(matrix)
            matrix = floodFill(matrix, row+1, column)
    except:
        pass
    # Go left
    try:
        if matrix[row][column-1] == base and column-1 >= 0:
            printMatrix(matrix)
            matrix = floodFill(matrix, row, column-1)
    except:
        pass

    return matrix


if __name__ == '__main__':

    columCount = 5
    rowCount = 4

    mat = [['.' for x in range(columCount)] for y in range(rowCount)]

    mat[2][0] = '|'
    mat[2][1] = '|'
    mat[3][1] = '|'

    for i, row in enumerate(mat):
        for j, elem in enumerate(row):
            if j == 4:
                mat[i][j] = '|'
            if i == 2:
                mat[i][j] = "|"
        # print(row)
    printMatrix(mat)
    print("================================")
    mat = floodFill(mat, 0, 1)
    printMatrix(mat)
