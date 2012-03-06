import collections


class Trainer:

    def __init__(self, nn, outputreversals, memorysize):
        self.nn = nn
        self.outputreversals = outputreversals
        self.memory = collections.deque([], memorysize) #input=>target store

    @staticmethod
    def _normalise(value):
        if value > 0.5:
            return 1
        return 0

    @staticmethod
    def _iterations(maxiters, quesize, index):
        return maxiters

    def getoutputs(self, inputs):
        return tuple(map(Trainer._normalise, self.nn.update(inputs)))

    def bad(self, inputs, outputs):
        outputs = tuple(map(Trainer._normalise, outputs))
        targets = self.outputreversals[outputs]
        self.memory.append((inputs, targets))

    def good(self, inputs, outputs):
        targets = tuple(map(Trainer._normalise, outputs))
        self.memory.append((inputs, targets))

    def train(self, iterations=1000):
        for i in range(len(self.memory)):
            for j in range(Trainer._iterations(iterations, self.memory.maxlen, i)):
                self.nn.update(self.memory[i][0])
                self.nn.backPropagate(self.memory[i][1], 0.5, 0.1)
