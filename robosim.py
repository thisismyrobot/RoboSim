import copy


class Terrain(object):

    FLOOR = 0
    WALL = 1
    ROBOT = 8


class Robot(object):
    """ A robot.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.hit = [False, False]

    def turnleft45(self):
        self.angle = Sim.fixangle(self.angle - 45)
        self._updatesensors()

    def turnright45(self):
        self.angle = Sim.fixangle(self.angle + 45)
        self._updatesensors()

    def turnleft90(self):
        self.angle = Sim.fixangle(self.angle - 90)
        self._updatesensors()

    def turnright90(self):
        self.angle = Sim.fixangle(self.angle + 90)
        self._updatesensors()

    def turn180(self):
        self.angle = Sim.fixangle(self.angle + 180)
        self._updatesensors()

    def _updatesensors(self):
        self.hit = [False, False]
        if not Sim.passable(Sim.location(self.x, self.y, Sim.fixangle(self.angle - 45))):
            self.hit[0] = True
        if not Sim.passable(Sim.location(self.x, self.y, Sim.fixangle(self.angle + 45))):
            self.hit[1] = True
        if ((self.hit == [False, False] and
             self.angle % 45 == 0 and not
             Sim.passable(Sim.location(self.x, self.y, self.angle)))
            or
            (self.angle % 45 != 0 and not
             Sim.passable(Sim.location(self.x, self.y, self.angle)))):
             self.hit = [True, True]

    def forward(self):
        x, y = Sim.location(self.x, self.y, self.angle)
        if Sim.passable((x, y)):
            self.x = x
            self.y = y
        self._updatesensors()


class SimMeta(type):
    def __str__(self):
        mapcopy = copy.deepcopy(Sim.mapdata)
        mapcopy[Sim.robot.y][Sim.robot.x] = "R"
        visual = ""
        visual += "/".ljust(Sim.mapwidth + 1, "-") + "\\\n"
        for row in range(Sim.mapheight):
            for col in range(Sim.mapwidth):
                if col == 0:
                    visual += "|"
                visual += str(mapcopy[row][col])
                if col == Sim.mapwidth - 1:
                    visual += "|"
            visual += "\n"
        visual += "\\".ljust(Sim.mapwidth + 1, "-") + "/"
        return visual


class Sim(object):
    """ A very basic robot simulator. Robot moves forward or backward, in one
        of 8 directions (chosen by rotating on spot).
    """

    __metaclass__ = SimMeta

    @staticmethod
    def setup(mapdata, robot):
        """ Setup, load the mapfile.
        """
        Sim.mapdata = mapdata
        Sim.mapwidth = len(mapdata[0])
        Sim.mapheight = len(mapdata)
        Sim.robot = robot

    @staticmethod
    def passable(xy):
        x = xy[0]
        y = xy[1]
        return (x >= 0 and y >= 0 and
                x < Sim.mapwidth and y < Sim.mapheight and
                Sim.mapdata[y][x] == Terrain.FLOOR)

    @staticmethod
    def fixangle(angle):
        if angle < 0:
            angle += 360
        if angle > 360:
            angle -= 360
        if angle == 360:
            angle = 0
        return angle

    @staticmethod
    def location(x, y, direction):
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
