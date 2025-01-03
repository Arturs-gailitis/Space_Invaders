from turtle import *
import math
import random
from abc import *

class LaserCannon(Turtle):
    def __init__(self, xMin, xMax, yMin, yMax):
        super().__init__()
        self.__xMin = xMin
        self.__xMax = xMax
        self.__yMin = yMin
        self.__yMax = yMax
        self.__screen = self.getscreen()
        self.__screen.onkey(self.turn_left, 'Left')  # Bind left arrow key
        self.__screen.onkey(self.turn_right, 'Right')  # Bind right arrow key
        self.__screen.onkey(self.shoot, 's')  # Bind 's' key to shoot
        self.__screen.onkey(self.quit, 'q')  # Bind 'q' key to quit

    def turn_left(self):
        self.left(15)  # Turn left by 15 degrees

    def turn_right(self):
        self.right(15)  # Turn right by 15 degrees

    def shoot(self):
        Bomb(self.heading(), 5, self.__xMin, self.__xMax, 
                                self.__yMin, self.__yMax)

    def quit(self):
        self.__screen.bye()

class BoundedTurtle(Turtle):
    def __init__(self, speed, xMin, xMax, yMin, yMax):
        super().__init__()
        self.__xMin = xMin
        self.__xMax = xMax
        self.__yMin = yMin
        self.__yMax = yMax
        self.__speed = speed

    def outOfBounds(self):
        xPos, yPos = self.position()
        out = False
        if xPos < self.__xMin or xPos > self.__xMax:
            out = True
        if yPos < self.__yMin or yPos > self.__yMax:
            out = True
        return out

    def getSpeed(self):
        return self.__speed

    @abstractmethod  
    def remove(self):
        pass

    @abstractmethod
    def move(self):
        pass

class Drone(BoundedTurtle):
    droneList = []  # Static variable

    @staticmethod
    def getDrones():
        return [x for x in Drone.droneList if x.__alive]

    def __init__(self, speed, xMin, xMax, yMin, yMax):
        super().__init__(speed, xMin, xMax, yMin, yMax)
        self.getscreen().tracer(0)
        self.up()
        if 'Drone.gif' not in self.getscreen().getshapes():
            self.getscreen().addshape('Drone.gif')
        self.shape('Drone.gif')
        self.goto(random.randint(xMin + 20, xMax - 20), yMax - 20)
        self.setheading(random.randint(250, 290))
        self.getscreen().tracer(1)
        Drone.droneList.append(self)
        self.__alive = True
        self.getscreen().ontimer(self.move, 200)

    def move(self):
        self.forward(self.getSpeed())
        if self.outOfBounds():
            DroneInvasion.update_score(-5)  # Lose 5 points for escaping drone
            self.remove()
        else:
            self.getscreen().ontimer(self.move, 200)

    def remove(self):
        self.__alive = False
        self.hideturtle()

class Bomb(BoundedTurtle):
    def __init__(self, initHeading, speed, xMin, xMax, yMin, yMax):
        super().__init__(speed, xMin, xMax, yMin, yMax)
        self.resizemode('user')
        self.color('red', 'red')
        self.shape('circle')
        self.turtlesize(.25)
        self.setheading(initHeading)
        self.up()        
        self.getscreen().ontimer(self.move, 100)

    def move(self):
        exploded = False
        self.forward(self.getSpeed())
        for a in Drone.getDrones():
            if self.distance(a) < 10:  # Adjusted collision range
                a.remove()
                DroneInvasion.update_score(5)  # Gain 5 points for hitting a drone
                exploded = True
        if self.outOfBounds() or exploded:
            self.remove()
        else:
            self.getscreen().ontimer(self.move, 100)

    def distance(self, other):
        p1 = self.position()
        p2 = other.position()        
        return math.dist(p1, p2)

    def remove(self):
        self.hideturtle()

class DroneInvasion:
    score = 0  # Class variable to keep track of score
    score_turtle = None  # Shared turtle to display the score

    def __init__(self, xMin, xMax, yMin, yMax):
        self.__xMin = xMin
        self.__xMax = xMax
        self.__yMin = yMin
        self.__yMax = yMax

    def play(self):
        self.__mainWin = LaserCannon(self.__xMin, self.__xMax,
                                self.__yMin, self.__yMax).getscreen()
        self.__mainWin.bgcolor('light green')
        self.__mainWin.setworldcoordinates(self.__xMin, self.__yMin, 
                                           self.__xMax, self.__yMax)
        DroneInvasion.score_turtle = Turtle()
        DroneInvasion.score_turtle.hideturtle()
        DroneInvasion.score_turtle.up()
        DroneInvasion.score_turtle.goto(self.__xMin + 10, self.__yMax - 20)
        DroneInvasion.update_score(0)  # Initialize score display
        self.__mainWin.ontimer(self.addDrone, 1000)
        self.__mainWin.listen()
        mainloop()

    def addDrone(self):
        if len(Drone.getDrones()) < 7:
            Drone(1, self.__xMin, self.__xMax, 
                     self.__yMin, self.__yMax)
        self.__mainWin.ontimer(self.addDrone, 1000)

    @staticmethod
    def update_score(points):
        DroneInvasion.score += points
        DroneInvasion.score_turtle.clear()
        DroneInvasion.score_turtle.write(f"Score: {DroneInvasion.score}", 
                                         font=("Arial", 16, "bold"))

# Main method to run the game
def main():
    xMin, xMax, yMin, yMax = -200, 200, -200, 200  # Game boundaries
    game = DroneInvasion(xMin, xMax, yMin, yMax)
    game.play()

if __name__ == "__main__":
    main()
