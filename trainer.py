import collections
import random


class Trainer:
    """ Order of ops:
         1. __init__()
         2. getoutput()
         3. good() or bad()
    """

    def __init__(self, nn, memorysize, statesets, seed=None):

        if seed is None:
            random.seed()
        else:
            random.seed(seed)

        self.nn = nn
        self.nn.setup_weights()

        self.memory = collections.deque([], memorysize) # {input:target} store
        self.statesets = statesets

        self._lastinput = [0]*len(self.nn.ai)
        self._lastoutput = [0]*len(self.nn.ao)

    @property
    def _freeoutputs(self):
        stateoutputs = []
        for sset in self.statesets:
            stateoutputs.extend(range(sset[0], sset[1] + 1))
        return [i for i in range(len(self.nn.ao)) if i not in stateoutputs]

    def _mutate(self):
        for i in self._freeoutputs:
            if random.random() > 0.75:
                self._lastoutput[i] = random.random()
        for s in self.statesets:
            if random.random() > 0.75:
                for i in range(s[0], s[1] + 1):
                    self._lastoutput[i] = 0
                self._lastoutput[random.randint(s[0], s[1])] = random.random()

    @staticmethod
    def _normalise(value):
        if value >= 0.5:
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
