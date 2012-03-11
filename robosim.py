import copy


class Terrain:

    FLOOR = 0
    WALL = 1
    ROBOT = 8


class Robot:
    """ A very basic robot simulator. Robot moves forward or backward, in one
        of 8 directions (chosen by rotating on spot).
    """

    def __init__(self, size, mapdata, x, y):
        """ Setup, load the mapfile.
        """
        self.mapdata = mapdata
        self.mapwidth = len(self.mapdata)
        self.mapheight = len(self.mapdata[0])
        self.angle = 0
        self.x = x
        self.y = y
        self.hit = [False, False]

    @property
    def state(self):
        mapcopy = copy.deepcopy(self.mapdata)
        mapcopy[self.y][self.x] = Terrain.ROBOT
        return mapcopy

    def _fixangle(self, angle):
        if angle < 0:
            angle += 360
        if angle > 360:
            angle -= 360
        if angle == 360:
            angle = 0
        return angle

    def _passable(self, xy):
        x = xy[0]
        y = xy[1]
        return (x >= 0 and y >= 0 and
                x < self.mapwidth and y < self.mapheight and
                self.mapdata[y][x] in (Terrain.ROBOT, Terrain.FLOOR))

    def turnleft45(self):
        self.angle = self._fixangle(self.angle - 45)
        self._updatesensors()

    def turnright45(self):
        self.angle = self._fixangle(self.angle + 45)
        self._updatesensors()

    def turnleft90(self):
        self.angle = self._fixangle(self.angle - 90)
        self._updatesensors()

    def turnright90(self):
        self.angle = self._fixangle(self.angle + 90)
        self._updatesensors()

    def turn180(self):
        self.angle = self._fixangle(self.angle + 180)
        self._updatesensors()

    def _updatesensors(self):
        self.hit = [False, False]
        if not self._passable(self._location(self.x, self.y, self._fixangle(self.angle - 45))):
            self.hit[0] = True
        if not self._passable(self._location(self.x, self.y, self._fixangle(self.angle + 45))):
            self.hit[1] = True
        if ((self.hit == [False, False] and
             self.angle % 45 == 0 and not
             self._passable(self._location(self.x, self.y, self.angle)))
            or
            (self.angle % 45 != 0 and not
             self._passable(self._location(self.x, self.y, self.angle)))):
             self.hit = [True, True]

    def _location(self, x, y, direction):
        if direction == 0:
            y-=1
        if direction == 45:
            x+=1
            y-=1
        if direction == 90:
            x+=1
        if direction == 135:
            x+=1
            y+=1
        if direction == 180:
            y+=1
        if direction == 225:
            x-=1
            y+=1
        if direction == 270:
            x-=1
        if direction == 315:
            x-=1
            y-=1
        return x, y

    def forward(self):
        x, y = self._location(self.x, self.y, self.angle)
        if self._passable((x, y)):
            self.x = x
            self.y = y
        self._updatesensors()
