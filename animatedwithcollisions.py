from turtle import Turtle, mainloop
import random

class AnimatedTurtle(Turtle):

    __allTurtles = []

    def __init__(self, hWall, vWall):
        super().__init__()
        self.__scr = self.getscreen()
        self.__xMin = -vWall + 10
        self.__xMax = vWall - 10
        self.__yMin = -hWall + 10
        self.__yMax = hWall - 10
        self.__scr.ontimer(self.__moveOneStep, 100)
        AnimatedTurtle.__allTurtles.append(self)

    def __moveOneStep(self):
        self.__computeNewHeading()
        self.forward(5)
        self.__checkCollisions()
        self.__scr.ontimer(self.__moveOneStep, 100)

    def __computeNewHeading(self):
        xPos, yPos = self.position()
        oldHead = self.heading()
        newHead = oldHead

        if xPos > self.__xMax or xPos < self.__xMin:
            newHead = 180 - oldHead
        if  yPos > self.__yMax or yPos < self.__yMin:
            newHead = 360 - oldHead
        if newHead != oldHead:
            self.setheading(newHead)

    def __checkCollisions(self):
        for otherT in AnimatedTurtle.__allTurtles:
            if self != otherT:
                if self.distance(otherT) < 20:#if close, swap headings
                    tempHeading = self.heading()
                    self.setheading(otherT.heading())
                    otherT.setheading(tempHeading)
                    while self.distance(otherT) < 20: #move away
                        self.forward(1)
                        otherT.forward(1)


class TurtlePlace:
    def __init__(self, maxTurtles, hWall = 200, vWall = 200):
        self.__bigT = Turtle()
        self.__bigTscreen = self.__bigT.getscreen()
        self.__bigT.color('blue')
        self.__turtleList = []
        self.__bigTscreen.onclick(self.placeTurtle)
        self.__bigT.hideturtle()
        self.__numTurtles = 0
        self.__maxTurtles = maxTurtles
        self.__hWall = hWall
        self.__vWall = vWall
        self.drawField()
        mainloop()

    def placeTurtle(self, x, y):
        newT = AnimatedTurtle(self.__hWall, self.__vWall)        
        newT.hideturtle()
        newTscreen = newT.getscreen()
        newTscreen.tracer(0)
        newT.up()
        newT.goto(x, y)
        newT.shape('turtle')
        newT.color('green')
        newT.showturtle()
        newT.setheading(random.randint(1, 359))
        newTscreen.tracer(1)
        self.__numTurtles = self.__numTurtles + 1
        self.__turtleList.append(newT)
        if self.__numTurtles >= self.__maxTurtles:
            self.__bigTscreen.onclick(None) #remove event handler

    def drawField(self):
        self.__bigTscreen.tracer(0)
        self.__bigT.up()
        self.__bigT.goto(-(self.__hWall), -(self.__vWall))
        self.__bigT.down()
        for i in range(4):
            self.__bigT.forward(2 * self.__hWall)
            self.__bigT.left(90)
        self.__bigTscreen.tracer(1)
