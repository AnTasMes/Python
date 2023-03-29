import numpy as np


class Map:
    def __init__(self, x: int, y: int) -> None:
        self.xVal = x
        self.yVal = y
        self.makeSelf(self.xVal, self.yVal)

    def makeSelf(self, x, y):
        self.mapMatrix = np.array([["." for i in range(x)] for j in range(y)])

    def printMap(self):
        top = np.array([f"{i}" for i in range(self.xVal)])
        print("\n\n   ", top)
        for i in range(len(self.mapMatrix)):
            print(f"[{i}]", self.mapMatrix[i])

    def setStart(self, x, y):
        try:
            self.mapMatrix[x][y] = "S"
        except:
            print("Values outside of bounds")
            self.printMap()

    def setEnd(self, x, y):
        try:
            self.mapMatrix[x][y] = "E"
        except:
            print("Values outside of bounds")
            self.printMap()

    def drawWalls(self, x: int, y: int, direction: str, ch="0"):
        # directions: d, u, l, r
        try:
            if self.mapMatrix[x][y] == "S":
                return
            if x + 1 <= self.xVal and direction == "d":
                self.drawWalls(x + 1, y, "d")
            elif x - 1 >= 0 and direction == "u":
                self.drawWalls(x - 1, y, "u")
            elif y + 1 <= self.yVal and direction == "r":
                self.drawWalls(x, y + 1, "r", ch="_")
            elif y - 1 >= 0 and direction == "l":
                self.drawWalls(x, y - 1, "l", ch="_")
        except:
            pass

        self.mapMatrix[x][y] = ch


if __name__ == "__main__":
    m = Map(10, 10)
    m.setStart(5, 2)
    m.setEnd(10, 8)
    m.drawWalls(5, 5, "l")
    m.printMap()
