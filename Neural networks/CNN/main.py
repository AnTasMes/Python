from mnist import MNIST as mn
from flex_a_fun import Activation as af

import matplotlib.pyplot as plt
import numpy as np
import sys


class Model:
    def __init__(self) -> None:
        self.model = []
        self.filter_list = []

    def add_layer(self, obj: object):
        self.model.append(obj)

    def add_filter(self, filter: np.ndarray, num_channels: int):
        if num_channels == 1:
            self.filter_list.append(np.reshape(
                filter, (filter.shape[0], filter.shape[1], 1)))
        elif num_channels > 1:
            pass

    def process(self, data: np.ndarray):
        for i in self.model:
            if type(i) == Convolution2D:
                i._convolve(data, self.filter_list)
            elif type(i) is Pooling2D:
                pass

    @staticmethod
    def gen_image(arr: np.ndarray) -> plt:
        two_d = (np.reshape(arr, (arr.shape[0], arr.shape[1])) * 255)
        plt.imshow(two_d, cmap='gray')
        return plt


class Convolution2D:
    def __init__(self, batch_size: int, width: int, height: int, num_channels: int) -> None:
        self.num_channels = num_channels
        self.batch_size = batch_size
        self.width = width
        self.height = height

    def _convolve(self, data: np.ndarray, filter_list: np.ndarray):
        self.filter_list = filter_list
        self.data = data

        output = []
        for index, filter in enumerate(self.filter_list):
            if self.num_channels != filter.shape[-1]:
                print("Error: Numbers of channels must match between filters and batch")
                sys.exit()

            if self.num_channels == 1:
                pass
                # output.append(self._conv())
                # srediti _conv i ostaviti mogucnost da se ne radi sve u jednoj funkciji (_conv)

            elif self.num_channels > 1:
                for i in self.num_channels:
                    output.append(self._conv(i))

    def _conv(self, img: np.ndarray, cr_f: np.ndarray, channel: int):
        start_range = coord_shift = np.uint16(cr_f.shape[0] / 2)
        stop_range = np.uint16(img.shape[0] - cr_f.shape[0] / 2 + 1)

        result = np.zeros((img.shape[0] - cr_f.shape[0] + 1,
                           img.shape[1] - cr_f.shape[0] + 1))

        for i in np.arange(start_range, stop_range):
            for j in np.arange(start_range, stop_range):
                chunk = img[i-coord_shift:i-coord_shift+cr_f.shape[0],
                            j-coord_shift:j-coord_shift+cr_f.shape[0], 0]

                result[i-1][j-1] = np.sum(chunk * cr_f[:, :, channel])

        return result


class Pooling2D:
    def __init__(self, width: int, height: int, mode: str) -> None:
        self.width = width
        self.height = height
        self.mode = mode

    def _pooling(self, data: np.ndarray):
        self.data = data

    def _pool(self):
        pass


def gen_data(data, width: int, height: int, num_channels: int, count: int) -> np.ndarray:
    images = []
    for i in range(count):
        shaping = np.reshape(data[i], (width, height))
        tmp = np.zeros((width, height, num_channels))
        if num_channels == 1:
            tmp[:, :, 0] = shaping[:]

        images.append(tmp)

    return images


def main():
    mndata = mn('samples')

    images, labels = mndata.load_training()

    filter_1 = np.array([
        [1, -1, 0],
        [1, -1, 0],
        [1, -1, 0]
    ])
    filter_2 = np.array([
        [0, -1, 1],
        [0, -1, 1],
        [0, -1, 1]
    ])
    filter_3 = np.array([
        [0, 0, 0],
        [-1, -1, -1],
        [1, 1, 1]
    ])
    filter_4 = np.array([
        [1, 1, 1],
        [-1, -1, -1],
        [0, 0, 0]
    ])
    filter_5 = np.array([
        [1, 1, 1],
        [1, -1, 1],
        [1, 1, 1]
    ])

    b_size = 5
    data = gen_data(images, 28, 28, 1, b_size)

    model = Model()

    model.add_filter(filter_1, 1)
    model.add_filter(filter_2, 1)
    model.add_filter(filter_3, 1)
    model.add_filter(filter_4, 1)
    model.add_filter(filter_5, 1)

    #print(model.filter_list[2][:, :, 0])
    model.add_layer(Convolution2D(b_size, 28, 28, 1))
    model.process(data)


if __name__ == '__main__':
    main()
