"""backprop_network.py"""import randomimport numpy as npimport mathclass Network(object):    def __init__(self, sizes):        """The list ``sizes`` contains the number of neurons in the        respective layers of the network.  For example, if the list        was [2, 3, 1] then it would be a three-layer network, with the        first layer containing 2 neurons, the second layer 3 neurons,        and the third layer 1 neuron.  The biases and weights for the        network are initialized randomly, using a Gaussian        distribution with mean 0, and variance 1.  Note that the first        layer is assumed to be an input layer, and by convention we        won't set any biases for those neurons, since biases are only        ever used in computing the outputs from later layers."""        self.num_layers = len(sizes)        self.sizes = sizes        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]    def SGD(self, training_data, epochs, mini_batch_size, learning_rate, test_data):        """Train the neural network using mini-batch stochastic        gradient descent.  The ``training_data`` is a list of tuples        ``(x, y)`` representing the training inputs and the desired        outputs.  """        print("Initial test accuracy: {0}".format(self.one_label_accuracy(test_data)))        n = len(training_data)        for j in range(epochs):            random.shuffle(training_data)            mini_batches = [training_data[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]            for mini_batch in mini_batches:                self.update_mini_batch(mini_batch, learning_rate)            print ("Epoch {0} test accuracy: {1}".format(j, self.one_label_accuracy(test_data)))    def update_mini_batch(self, mini_batch, learning_rate):        """Update the network's weights and biases by applying        stochastic gradient descent using backpropagation to a single mini batch.        The ``mini_batch`` is a list of tuples ``(x, y)``."""        nabla_b = [np.zeros(b.shape) for b in self.biases]        nabla_w = [np.zeros(w.shape) for w in self.weights]        for x, y in mini_batch:            delta_nabla_b, delta_nabla_w = self.backprop(x, y)            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]        self.weights = [w - (learning_rate / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)]        self.biases = [b - (learning_rate / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)]    def backprop(self, x, y):        """The function receives as input a 784 dimensional         vector x and a one-hot vector y.        The function should return a tuple of two lists (db, dw)        as described in the assignment pdf. """        # Forward Pass        # Forward Pass        z = [np.array([]) for _ in range(self.num_layers)]        v = [np.array([]) for _ in range(self.num_layers)]        z[0] = x.reshape(-1, 1)        v[0] = x.reshape(-1, 1)        for l in range(0, self.num_layers - 2):            v[l + 1] = np.matmul(self.weights[l], z[l].reshape(-1, 1)) + self.biases[l]            z[l + 1] = relu(v[l + 1]).reshape(-1, 1)        v[self.num_layers - 1] = np.matmul(self.weights[self.num_layers - 2], z[self.num_layers - 2].reshape(-1, 1)) + \                                 self.biases[self.num_layers-2]        z[self.num_layers - 1] = self.output_softmax(v[self.num_layers - 1])        #         return z        dw = [np.array([]) for _ in range(len(self.weights))]        db = [np.array([]) for _ in range(len(self.biases))]        delta_l = [np.array([]) for _ in range(self.num_layers)]        delta_L_W = np.matmul((z[self.num_layers - 1] - y.reshape(-1,1)), z[self.num_layers - 2].T)  # last layer        delta_L_b = z[self.num_layers - 1] - y.reshape(-1, 1)  # last layer        dw[-1] = delta_L_W        db[-1] = delta_L_b        delta_l[-1] = z[self.num_layers - 1] - y.reshape(-1, 1)        for l in range(len(dw)-2, -1, -1):            delta_l[l+1] = np.matmul(self.weights[l+1].T,                                   np.multiply(relu_derivative(v[l + 2]), delta_l[l + 2]))            dw[l] = np.matmul(np.multiply(delta_l[l+1], relu_derivative(v[l+1])).reshape(-1,1), z[l].reshape(1, -1))            db[l] = np.multiply(delta_l[l+1], relu_derivative(v[l+1]))        return (db, dw)    def one_label_accuracy(self, data):        """Return accuracy of network on data with numeric labels"""        output_results = [(np.argmax(self.network_output_before_softmax(x)), y)         for (x, y) in data]        return sum(int(x == y) for (x, y) in output_results)/float(len(data))    def one_hot_accuracy(self,data):        """Return accuracy of network on data with one-hot labels"""        output_results = [(np.argmax(self.network_output_before_softmax(x)), np.argmax(y)) for (x, y) in data]        return sum(int(x == y) for (x, y) in output_results) / float(len(data))    def network_output_before_softmax(self, x):        """Return the output of the network before softmax if ``x`` is input."""        layer = 0        for b, w in zip(self.biases, self.weights):            if layer == len(self.weights) - 1:                x = np.dot(w, x) + b            else:                x = relu(np.dot(w, x)+b)            layer += 1        return x    def loss(self, data):        """Return the loss of the network on the data"""        loss_list = []        for (x, y) in data:            net_output_before_softmax = self.network_output_before_softmax(x)            net_output_after_softmax = self.output_softmax(net_output_before_softmax)            loss_list.append(np.dot(-np.log(net_output_after_softmax).transpose(),y).flatten()[0])        return sum(loss_list) / float(len(data))    def output_softmax(self, output_activations):        """Return output after softmax given output before softmax"""        output_exp = np.exp(output_activations)        return output_exp/output_exp.sum()    def loss_derivative_wr_output_activations(self, output_activations, y):        #TODO: Implement derivative of loss with respect to the output activations before softmax        return 1def relu(z):    return np.maximum(0,z)def relu_derivative(z):    """Gets a Vector. if z_i>0, then direvative is 1, else 0"""    return np.where(z>0, 1, 0)net = Network([2,3,2,2])db,dw = net.backprop(np.array([1,2]), np.array([0,1]))print("db: \n", db)print()for b in db:    print(b.shape)print()print("dw: \n",dw)print()for w in dw:    print(w.shape)