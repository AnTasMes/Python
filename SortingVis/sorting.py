import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os


figure = plt.figure()
ax = figure.add_subplot(111)


font = {'family': 'normal',
        'weight': 'bold',
        'size': 10}

plt.rc('font', **font)


class Sorting:
    def __init__(self, cl: object) -> None:
        self.obj = cl

    def animate(self, i):
        self.obj.animate(i)


class BubbleSort:
    _cntr = -1

    def __init__(self, arr) -> None:
        self.arr = arr
        self.max = len(arr)-2

    def retCurrIndex(self):
        if self._cntr >= -1 and self._cntr < self.max:
            self._cntr += 1
            return self._cntr, self._cntr + 1
        else:
            self._cntr = 0
            self.max -= 1
            return 0, 1

    def switch(self, index: tuple):
        if self.arr[index[0]] > self.arr[index[1]]:
            self.arr[index[0]], self.arr[index[1]
                                         ] = self.arr[index[1]], self.arr[index[0]]

    def isSorted(self):
        if self.max <= 0:
            return True
        return False

    def animate(self, i):
        F, L = self.retCurrIndex()

        ax.clear()
        ax.grid(True)
        ax.plot(self.arr, '--yo', markersize=2, linewidth=1)
        ax.plot(F, self.arr[F], 'ro')
        ax.plot(L, self.arr[L], 'go')

        ax.annotate(self.arr[F], (F, self.arr[F]))
        ax.annotate(self.arr[L], (L, self.arr[L]))

        self.switch((F, L))


if __name__ == '__main__':
    arr = np.random.randint(5, 200, 40)
    init_arr = arr[:]
    ani = animation.FuncAnimation(figure, Sorting(
        BubbleSort(arr)).animate, interval=1)
    plt.show()

    print(f'{init_arr} ==> {arr}')
