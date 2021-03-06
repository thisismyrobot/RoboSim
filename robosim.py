# Copyright 2012 Robert Wallhead
# robert@thisismyrobot.com
# <http://thisismyrobot.com>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy


class Terrain(object):

    FLOOR = 0
    WALL = 1
    ROBOT = 8


class Robot(object):
    """ A robot.
    """

    def __init__(self, x, y):
        """ set up the robot.
        """
        self.x = x
        self.y = y
        self.angle = 0
        self.hit = [False, False]

    def turn(self, ticks):
        """ Turns the robot by -4 -> +4 ticks, each tick is 45 degrees.
        """
        ticks = int(ticks)
        if ticks > 4:
            ticks = 4
        if ticks < -4:
            ticks = -4
        self.angle = self.sim.fixangle(self.angle + (45 * ticks))
        self._updatesensors()

    def move(self, direction):
        """ Moves the robot one step - 1=forward, -1=reverse.
        """
        x, y = 0, 0
        if direction == 1:
            x, y = self.sim.location(self.x, self.y, self.angle)
        elif direction == -1:
            x, y = self.sim.location(self.x, self.y,
                                     self.sim.fixangle(self.angle + 180))
        else:
            return
        if self.sim.passable((x, y)):
            self.x = x
            self.y = y
        self._updatesensors()

    def _updatesensors(self):
        """ Update the status of the sensors based on location.
        """
        sim, x, y, angle = self.sim, self.x, self.y, self.angle
        self.hit = [False, False]
        if not sim.passable(sim.location(x, y, sim.fixangle(angle - 45))):
            self.hit[0] = True
        if not sim.passable(sim.location(x, y, sim.fixangle(angle + 45))):
            self.hit[1] = True
        if ((self.hit == [False, False] and self.angle % 45 == 0 and not
             self.sim.passable(sim.location(x, y, angle)))
            or
            (self.angle % 45 != 0 and not
             self.sim.passable(sim.location(x, y, angle)))):
            self.hit = [True, True]


class Sim(object):
    """ A very basic robot simulator. Robot moves forward or backward, in one
        of 8 directions (chosen by rotating on spot).
    """

    def __init__(self, mapdata):
        """ Setup the map from its data.
        """
        self.mapdata = mapdata
        self.mapwidth = len(mapdata[0])
        self.mapheight = len(mapdata)

    def __str__(self):
        """ Allows you to print the sim directly into a nice shiny ASCII
            graphic :)
        """
        mapcopy = copy.deepcopy(self.mapdata)
        mapcopy[self.robot.y][self.robot.x] = "R"

        visual = "X: " + str(self.robot.x) + "\n"
        visual += "Y: " + str(self.robot.y) + "\n"
        visual += "DIR: " + str(self.robot.angle) + "\n\n"
        visual += "/".ljust(self.mapwidth + 1, "-") + "\\\n"

        for row in range(self.mapheight):
            for col in range(self.mapwidth):
                if col == 0:
                    visual += "|"
                visual += str(mapcopy[row][col])
                if col == self.mapwidth - 1:
                    visual += "|"
            visual += "\n"

        visual += "\\".ljust(self.mapwidth + 1, "-") + "/"
        return visual

    def setrobot(self, robot):
        """ Set the robot that sim will use.
        """
        robot.sim = self
        self.robot = robot

    def passable(self, xy):
        """ Return whether a location is passable.
        """
        x = xy[0]
        y = xy[1]
        return (x >= 0 and y >= 0 and
                x < self.mapwidth and y < self.mapheight and
                self.mapdata[y][x] == Terrain.FLOOR)

    @staticmethod
    def fixangle(angle):
        """ Keep angles in the 0-359 range.
        """
        if angle < 0:
            angle += 360
        if angle > 360:
            angle -= 360
        if angle == 360:
            angle = 0
        return angle

    @staticmethod
    def location(x, y, direction):
        """ Get a location from an x, y, and direction.
        """
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
