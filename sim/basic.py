import copy


class Robot:
    """ A very basic robot simulator. Robot moves forward or backward, in one
        of 8 directions (chosen by rotating on spot).
    """

    FLOOR = 0
    WALL = 1
    ROBOT = 8

    def __init__(self, size, mapdata, x, y):
        """ Setup, load the mapfile.
        """
        self.size = size
        self.mapdata = mapdata
        self.angle = 0
        self.x = x
        self.y = y

    @property
    def state(self):
        mapcopy = copy.deepcopy(self.mapdata)
        mapcopy[self.y][self.x] = Robot.ROBOT
        return mapcopy

    def _fixangle(self):
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360
        if self.angle == 360:
            self.angle = 0

    def _index(self, x, y):
        return ((x % self.size) + 1) * ((y * self.size) + 1)

    def _passable(self, x, y):
        return self.mapdata[y][x] in (Robot.ROBOT, Robot.FLOOR)

    def turnleft45(self):
        self.angle -= 45
        self._fixangle()

    def turnright45(self):
        self.angle += 45
        self._fixangle()

    def turnleft90(self):
        self.angle -= 90
        self._fixangle()

    def turnright90(self):
        self.angle += 90
        self._fixangle()

    def turn180(self):
        self.angle += 180
        self._fixangle()

    def forward(self):
        x = self.x
        y = self.y
        if self.angle == 0:
            y-=1
        if self.angle == 45:
            x+=1
            y-=1
        if self.angle == 90:
            x+=1
        if self.angle == 135:
            x+=1
            y+=1
        if self.angle == 180:
            y+=1
        if self.angle == 225:
            x-=1
            y+=1
        if self.angle == 270:
            x-=1
        if self.angle == 315:
            x-=1
            y-=1
        if self._passable(x, y):
            self.x = x
            self.y = y
