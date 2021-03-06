A Python mobile robot simulator
===============================

A very very simple one at that :)

Note
----

Used to be part of https://github.com/thisismyrobot/BadDog

How to use
----------

Create a map - 0=floor, 1=interior wall. Map has automatic walls at bounds.

    >>> amap = [[0, 0, 0, 1, 0, 0, 0, 0],
    ...         [0, 0, 0, 0, 0, 0, 1, 1],
    ...         [0, 0, 1, 0, 0, 0, 0, 0]]

Create a simulation

    >>> import robosim
    >>> sim = robosim.Sim(amap)

Create a robot

    >>> robot = robosim.Robot(2, 2)

Add the robot to the simulation

    >>> sim.setrobot(robot)

Print out a pretty map view

    >>> print(sim)
    X: 2
    Y: 2
    DIR: 0
    <BLANKLINE>
    /--------\
    |00010000|
    |00000011|
    |00R00000|
    \--------/

Control the robot

    >>> sim.robot.move(1) # forward
    >>> sim.robot.turn(3) # clockwise 135 degrees
    >>> sim.robot.move(-1) # reverse
    >>> sim.robot.turn(-2) # anticlockwise 90 degrees

Read the two sensors on the front of the robot

    >>> print sim.robot.hit
    [True, False]

Read robotsim.txt for a more detailed doctest
