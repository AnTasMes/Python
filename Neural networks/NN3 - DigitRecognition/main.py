from mnist import MNIST as mn
from flex_a_fun import Activation
from Perceptron_FILE import Perceptron

import matplotlib.pyplot as plt
import numpy as np
import sys


class CNN:

    def __init__(self, input, filter_list: np.ndarray, activation: str = 'relu', padding: str = 'SamePadding', p_mode: str = 'max', count: int = 100) -> None:
        self.input = input
        self.filter_list = filter_list
        self.activation = activation
        self.padding = padding
        self.p_mode = p_mode

        self.data = self.prepare_data(count)

    def prepare_data(self, count: int):
        data = []
        for cnt in range(count):
            print(f'IMAGE: {cnt+1}')
            image = np.reshape(self.input[cnt], (28, 28))
            input = np.zeros((image.shape[0], image.shape[1], 2))

            input[:, :, 0] = image[:]
            features = self.convolution(
                input, self.filter_list, self.activation, self.padding)
            pooling = self.pooling(features, self.p_mode)

            features = self.convolution(
                features, self.filter_list, self.activation, self.padding)
            pooling = self.pooling(features, 'avg')

            data.append(pooling.flatten())
        return data

    @staticmethod
    def gen_image(arr: np.ndarray) -> plt:
        two_d = (np.reshape(arr, (arr.shape[0], arr.shape[1])) * 255)
        plt.imshow(two_d, cmap='gray')
        return plt

    def convolution(self, img: np.ndarray, filter_list: np.ndarray, activation: str = 'relu', padding: str = 'SamePadding') -> np.ndarray:
        """
        Function convolution maps all chunks of an input, calculates their filters,
        and maps them into a feature_map for that layer

        Feature_map is calculated like: `(img_w - filter_w + 1) x (img_h - filter_h + 1)` and `number_of_filters`

        Parameters
        ----------
        img : np.ndarray
            input data for calculating
        filter_list : np.ndarray
            Array of shape (`number_of_filters, wi, hi`)
        activation : str, optional
            String that defines which activation function will be used
        padding : str, optional
            String that defines if a padding will be used.
            `SamePadding` assures that the shape of feature maps will be the same as inputs.
            `ValidPadding` assures that the shape of feature maps will be `(img_w - filter_w + 1) x (img_h - filter_h + 1)`

        Functions
        ---------
        `_conv(img: np.ndarray, cr_f: np.ndarray)` -> np.ndarray
            returns an inside result of a filter layer

        Returns
        -------
        feature_map of type np.ndarray for later combinations

        Examples
        --------
        >>> features = convolution(input, filter, 'relu', 'SamePadding')
        >>> gen_image(features[:,:,0]).show()

        """
        if padding == 'SamePadding':
            npad = ((1, 1), (1, 1), (0, 0))
            img = np.pad(img, npad, mode='constant')

        feature_map = np.zeros((img.shape[0] - filter_list.shape[1] + 1,
                                img.shape[1] - filter_list.shape[2] + 1,
                                filter_list.shape[0]))

        for f_num, f in enumerate(filter_list):
            #print(f'Calculating for filter No. {f_num+1}')
            curr_filter = f
            if curr_filter.shape[0] != filter_list.shape[1] or curr_filter.shape[1] != filter_list.shape[2]:
                print(
                    f'Error: Filter doesnt match the shape of a filter list => {curr_filter.shape} : ({filter_list.shape[1:]})')
            if curr_filter.shape[0] % 2 == 0 or curr_filter.shape[1] % 2 == 0:
                print('Error: Filters must be an odd dimensional matrix')
                sys.exit()
            else:
                # adds results to a feature map of that layer
                feature_map[:, :, f_num] = self._conv(img, curr_filter)[:]

                # calculates the activation
                feature_map[:, :, f_num] = Activation(
                    prefix=activation).function(feature_map[:, :, f_num])

        return feature_map

    def _conv(self, img: np.ndarray, cr_f: np.ndarray) -> np.ndarray:
        """
        Calculates convolutions for a given filter and returns a result array

        Parameters
        ----------
        img : np.ndarray
            Input to be calculated
        cr_f : np.ndarray
            Current filter being in use for calculating

        Returns
        -------
        np.ndarray
            Single set of results from the input for a given filter
            Shape `(img_w - cr_f_w + 1, img_h - cr_f_w + 1)`
        """
        start_range = coord_shift = np.uint16(cr_f.shape[0] / 2)
        stop_range = np.uint16(img.shape[0] - cr_f.shape[0] / 2 + 1)

        result = np.zeros((img.shape[0] - cr_f.shape[0] + 1,
                           img.shape[1] - cr_f.shape[0] + 1))

        for i in range(start_range, stop_range):
            for j in range(start_range, stop_range):
                # separates each chunk by a filter
                chunk = img[i-coord_shift:i-coord_shift+cr_f.shape[0],
                            j-coord_shift:j-coord_shift+cr_f.shape[0], 0]
                # adds a result of a sum and multiplication with the filter to a result array
                result[i-1][j-1] = np.sum(chunk * cr_f)
        return result

    def _pool(self, cr_f_m: np.ndarray, mode: str, W: int, H: int) -> np.ndarray:
        """
        Does the actual pooling for a feature map

        Pool done with result[i//2][j//2] = np.mode(cr_f_m[i:i+2, j:j+2])
        i//2 and j//2 are halves of a current possition because pooling halves the map

        Parameters
        ----------
        cr_f_m : np.ndarray
            Current feature map to be pooled
        mode : str
            Mode with which the pooling is done
        W : int
            Width of the pooling map
        H : int
            Height of the pooling map

        Returns
        -------
        np.ndarray
            Result of pooling for that specific layer
        """
        result = np.zeros((W, H))

        for i in range(0, cr_f_m.shape[0] - 2, 2):
            for j in range(0, cr_f_m.shape[1] - 2, 2):
                if mode == 'max':
                    result[i//2][j//2] = np.max(cr_f_m[i:i+2, j:j+2])
                elif mode == 'min':
                    result[i//2][j//2] = np.min(cr_f_m[i:i+2, j:j+2])
                elif mode == 'avg':
                    result[i//2][j//2] = np.average(cr_f_m[i:i+2, j:j+2])
        return result

    def pooling(self, f_map: np.ndarray, mode: str) -> np.ndarray:
        """
        Calculates pool maps for layers of features

        Parameters
        ----------
        f_map : np.ndarray
            Features map of shape `(W, H, number_of_filters/maps)`
        mode : str
            Mode for which pooling will be done.
            `max` -> Maximum pooling
            `min` -> Minimum pooling
            `avg` -> Average pooling

        Returns
        -------
        np.ndarray
            Calculated pool map half the size of f_map
        """

        W, H, NUM = (np.uint16(f_map.shape[0]/2),
                     np.uint16(f_map.shape[1]/2), f_map.shape[-1])

        pool_map = np.zeros((W, H, NUM))

        for m_num in range(f_map.shape[-1]):
            curr_map = f_map[:, :, m_num]

            if mode not in ('max', 'min', 'avg'):
                print(f'Error: {mode} pooling is not supported')
                sys.exit()
            else:
                pool_map[:, :, m_num] = self._pool(curr_map, mode, W, H)[:]
        return pool_map


def main():
    mndata = mn('samples')

    images, labels = mndata.load_training()

    print(len(images[0]))
    image = np.reshape(images[1], (28, 28))
    input = np.zeros((image.shape[0], image.shape[1], 1))
    # input = np.zeros((image.shape[0], image.shape[1], channel_size))

    input[:, :, 0] = image[:]

    #CNN.gen_image(input[:, :, 0]).show()

    l1_filter = np.zeros((4, 3, 3))

    l1_filter[0, :, :] = np.array([[
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]]])

    l1_filter[1, :, :] = np.array([[
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]]])

    l1_filter[2, :, :] = np.array([[
        [1, 1, 1],
        [0, 0, 0],
        [-1, -1, -1]]])

    l1_filter[3, :, :] = np.array([[
        [-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1]]])
    # data = np.array([CNN(input, l1_filter, 'relu').data])

    training_output = []
    #CNN.gen_image(input[:, :, 0]).show()
    # print(output[0])
    for i in range(10):
        output = [0 for i in range(10)]
        output[labels[i]] = 1
        training_output.append(output)

    # print(training_output)

    training_input = np.array(CNN(images, l1_filter, count=10).data)
    training_output = np.array(training_output)
    # print(training_input[0])

    activation_dict = {
        '0': 'sigmoid',
        '1': 'sigmoid',
        '2': 'sigmoid'
    }
    # print(training_input[0].shape)
    # print(training_input[0])

    perc = Perceptron(training_input.shape[1], [
                      training_input.shape[1]//2, training_input.shape[1]//2], 10, fun=activation_dict)
    # print('TI: ', training_input.shape)
    # print('SW: ', perc.Synaptic_Weights[2].shape)
    perc.Train(training_input, training_output, 20000)
    res = perc.FeedForwardFlex(np.array([training_input[1]]).T, vb=1)
    CNN.gen_image(input[:, :, 0]).show()
    print(res[-1])
    # print(data)
    # features = convolution(input, l1_filter)
    # pools = pooling(features, mode='max')
    # print(len(pools.flatten()))

    # features = convolution(pools, l1_filter)

    # l1_filter[0, :, :] = np.array([[
    #     [-1, 0, 1],
    #     [-1, 0, 1],
    #     [-1, 0, 1]]])

    # l1_filter[0] = np.pad(l1_filter[0], 1)

    # print(l1_filter[0, :, :])

    # for p in range(pools.shape[-1]):
    #     gen_image(pools[:, :, p]).show()

    # for i in range(features.shape[-1]):
    #     gen_image(features[:, :, i]).show()

    # filter = np.array([[1, 1, 1, 1], [0, 0, 0, 0], [-1, -1, -1, -1]])

    # filter = np.pad(filter, 1, mode='constant')

    # for i in range(0, filter.shape[0]-2, 2):
    #     for j in range(0, filter.shape[1]-2, 2):
    #         print(np.max(filter[i:i+2, j:j+2]))
    #     print


if __name__ == '__main__':
    main()


# TO DO LIST:
# Srediti ovo da bude klasa
# Povezati sa Perceptron-om
# Omoguciti racunanje vise kanala (RGB)
