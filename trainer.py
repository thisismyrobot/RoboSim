import collections
import random


class Trainer:

    def __init__(self, nn, memorysize, whitelist):
        self.nn = nn
        self.memory = collections.deque([], memorysize) # {input:target} store
        self.whitelist = whitelist

    @staticmethod
    def _normalise(value):
        if value > 0.5:
            return 1
        return 0

    @staticmethod
    def _invert(outputs):
        """ Inverts the highest value in a tuple.
        """
        outputs = list(outputs)
        maxval = max(outputs)
        index = outputs.index(maxval)
        outputs[index] = 1 - maxval
        return tuple(outputs)

    def _whitelist(self, output):
        if output not in self.whitelist:
            output = random.choice(self.whitelist)
        return output

    def getoutput(self, inputs):
        output = self._whitelist(tuple(map(Trainer._normalise, self.nn.update(inputs))))
        return output

    def bad(self, inputs):
        targets = tuple(map(Trainer._normalise, Trainer._invert(self.nn.ao)))
        self.memory.append((inputs, targets))

    def good(self, inputs):
        targets = tuple(map(Trainer._normalise, self.nn.ao))
        self.memory.append((inputs, targets))

    def train(self, iterations=1000):
        for j in range(iterations):
            for i in range(len(self.memory)):
                self.nn.update(self.memory[i][0])
                self.nn.backPropagate(self.memory[i][1], 0.5, 0.1)
