import collections
import random


class Trainer:
    """ Order of ops:
         1. __init__()
         2. getoutput()
         3. good() or bad()
    """

    def __init__(self, nn, memorysize, seed):

        if seed is None:
            random.seed()
        else:
            random.seed(seed)

        self.nn = nn
        self.nn.setup_weights()

        self.memory = collections.deque([], memorysize) # {input:target} store
        self._lastinput = [0]*len(self.nn.ai)
        self._lastoutput = [0]*len(self.nn.ao)

    def _mutate(self):
        self._lastoutput = [random.random()
                            if random.random() > 0.75 else o
                            for o
                            in self._lastoutput]

    @staticmethod
    def _normalise(value):
        if value > 0.5:
            return 1
        return 0

    def getoutput(self, inputs=None):
        if inputs is None:
            inputs = self._lastinput
        else:
            self._lastinput = inputs
        self._lastoutput = self.nn.update(inputs)
        return tuple(map(Trainer._normalise, self._lastoutput))

    def good(self, iterations=1000):
        """ Add the input-output mapping to a memory buffer for training, do
            the training
        """
        self.memory.append((self._lastinput,
                            tuple(map(Trainer._normalise, self._lastoutput))))
        for j in range(iterations):
            for i in range(len(self.memory)):
                self.nn.update(self.memory[i][0])
                self.nn.backPropagate(self.memory[i][1], 0.5, 0.1)

    def bad(self):
        self._mutate()
        return tuple(map(Trainer._normalise, self._lastoutput))
