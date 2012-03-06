import collections


class Trainer:

    def __init__(self, nn, memorysize):
        self.nn = nn
        self.memory = collections.deque([], memorysize) # {input:target} store

    @staticmethod
    def _normalise(value):
        if value > 0.5:
            return 1
        return 0

    @staticmethod
    def _reverse(value):
        return 1 - value

    def getoutput(self, inputs):
        return tuple(map(Trainer._normalise, self.nn.update(inputs)))

    def bad(self, inputs, outputs):
        targets = tuple(map(Trainer._reverse, outputs))
        self.memory.append((inputs, targets))

    def good(self, inputs, outputs):
        targets = tuple(outputs)
        self.memory.append((inputs, targets))

    def train(self, iterations=1000):
        for j in range(iterations):
            for i in range(len(self.memory)):
                self.nn.update(self.memory[i][0])
                self.nn.backPropagate(self.memory[i][1], 0.5, 0.1)
