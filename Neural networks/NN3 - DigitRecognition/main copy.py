
import os

import matplotlib
from flex_a_fun import Activation
from Perceptron_FILE import Perceptron

from mnist.loader import MNIST as mn

import matplotlib.pyplot as plt
import numpy as np
import sys

class CNN_Layer:

    def __init__(self, filter_list: np.ndarray, activation: str = 'relu', padding: str = 'SamePadding', p_mode: str = 'max') -> None:
        self.filter_list = filter_list
        self.activation = activation
        self.padding = padding
        self.p_mode = p_mode


    def prepare(self, input):
        features = self.convolution(input)
        pooling = self.pooling(features)

        return pooling

    def convolution(self, img: np.ndarray) -> np.ndarray:
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
        
        if self.padding == 'SamePadding':
            npad = ((1, 1), (1, 1), (0, 0))
            img = np.pad(img, npad, mode='constant')

        feature_map = np.zeros((img.shape[0] - self.filter_list.shape[1] + 1,
                                img.shape[1] - self.filter_list.shape[2] + 1,
                                self.filter_list.shape[0] * img.shape[-1]))

        for i_num, i in enumerate(img.T):
            for f_num, f in enumerate(self.filter_list):

                index = f_num + (i_num * self.filter_list.shape[0])

                curr_filter = f
                if curr_filter.shape[0] != self.filter_list.shape[1] or curr_filter.shape[1] != self.filter_list.shape[2]:
                    print(
                        f'Error: Filter doesnt match the shape of a filter list => {curr_filter.shape} : ({self.filter_list.shape[1:]})')
                if curr_filter.shape[0] % 2 == 0 or curr_filter.shape[1] % 2 == 0:
                    print('Error: Filters must be an odd dimensional matrix')
                    sys.exit()
                else:
                    # adds results to a feature map of that layer

                    feature_map[:, :, index] = self._conv(i, curr_filter)[:]

                    # calculates the activation
                    feature_map[:, :, index] = Activation(
                        prefix=self.activation).function(feature_map[:, :, index])

        return feature_map
    
    def pooling(self, f_map: np.ndarray) -> np.ndarray:
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

            if self.p_mode not in ('max', 'min', 'avg'):
                print(f'Error: {self.p_mode} pooling is not supported')
                sys.exit()
            else:
                pool_map[:, :, m_num] = self._pool(curr_map, self.p_mode, W, H)[:]
        return pool_map 
    
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
                            j-coord_shift:j-coord_shift+cr_f.shape[0]]
                
                # aproximate between 0 and 1
                #chunk = chunk / 255

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

class CNN:

    def __init__(self, layers: list[CNN_Layer]) -> None:
        self.layers = layers

    def prepare_data(self, input_data, count: int = 100):
        output_data = []
        print('Preparing data...')
        for cnt in range(count):
            # print(f'IMAGE: {cnt+1}')
            image = np.reshape(input_data[cnt], (28, 28))
            input = np.zeros((image.shape[0], image.shape[1], 1))

            input[:, :, 0] = image[:]

            

            if cnt % 100 == 0:
                print(f'IMAGE: {cnt+1}')

            for layer in self.layers:
                input = layer.prepare(input)

            output_data.append(input.flatten())

        print('Data prepared!')

        output_data = np.array(output_data)

        # limit output to 0 and 1
        output_data[output_data > 1] = 1
        output_data[output_data < 0] = 0
        
        return output_data

    @staticmethod
    def gen_image(arr: np.ndarray) -> plt:
        two_d = (np.reshape(arr, (arr.shape[0], arr.shape[1])) * 255)
        plt.imshow(two_d, cmap='gray')
        return plt



def main():

    mndata = mn(path=os.path.join(os.getcwd(), 'samples'), return_type='numpy')

    # print(os.path.join(os.getcwd(), 'samples'))

    images, labels = mndata.load_training()

    print(len(images[1]))
    
    image = np.reshape(images[0], (28, 28))

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
    
    train_image_count = 600
    training_output = []
    #CNN.gen_image(input[:, :, 0]).show()
    # print(output[0])
    for i in range(train_image_count):
        output = [0 for i in range(10)]
        output[labels[i]] = 1
        training_output.append(output)

    training_output = np.array(training_output)


    layer_1 = CNN_Layer(l1_filter, 'relu', 'SamePadding', 'max')
    layer_2 = CNN_Layer(l1_filter, 'relu', 'SamePadding', 'max')

    cnn_model = CNN([layer_1])

    training_input = cnn_model.prepare_data(images, train_image_count)

    activation_dict = {
        '0': 'sigmoid',
        '1': 'sigmoid',
        '2': 'sigmoid',
        '3': 'lrelu'
    }

    perc = Perceptron(fun=activation_dict, base_fun='sigmoid')\
                                                .setLayers( 
                                                    training_input.shape[1], [
                                                    training_input.shape[1]//2, 
                                                    training_input.shape[1]//2,
                                                    training_input.shape[1]//4],
                                                    10)\
                                                .setLearningRate(0.01)\
                                                .setWeights()\
                                                .setBias()\
                                                .build_me()
    
    
    print(training_input.shape, len(training_output))

    perc.Train(training_input, training_output, 10000)

    hits = 0

    testing_sample_count = 200

    testing_sample_data, testing_sample_labels = mndata.load_testing()
    testing_input = cnn_model.prepare_data(testing_sample_data, testing_sample_count)

    for i in range(testing_sample_count):
        res = perc.FeedForwardFlex(np.array([testing_input[i]]).T, vb=0)
        val = [int(i) for i in (res[-1] == np.max(res[-1]))]
        
        if val.index(1) == testing_sample_labels[i]:
            hits += 1
        else:
            print("Label: ", testing_sample_labels[i], "Output: ", val.index(1))
    
    print(f'Accuracy: {hits/testing_sample_count*100}%')

if __name__ == '__main__':
    main()
