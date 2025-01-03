from turtle import *
import random
from abc import ABC, abstractmethod

# LaserCannon Class
class LaserCannon(Turtle):
    def __init__(self, xMin, xMax, yMin, yMax):
        super().__init__()
        self.__xMin, self.__xMax = xMin, xMax
        self.__yMin, self.__yMax = yMin, yMax
        self.__screen = self.getscreen()
        self.__configure_controls()

    def __configure_controls(self):
        self.__screen.onkey(self.shoot, 's')
        self.__screen.onkey(self.quit, 'q')
        self.__screen.onkey(self.turn_left, 'Left')
        self.__screen.onkey(self.turn_right, 'Right')

    def turn_left(self):
        self.setheading(self.heading() + 10)

    def turn_right(self):
        self.setheading(self.heading() - 10)

    def shoot(self):
        Bomb(self.heading(), 5, self.__xMin, self.__xMax, self.__yMin, self.__yMax)

    def quit(self):
        self.__screen.bye()

# BoundedTurtle Abstract Class
class BoundedTurtle(Turtle, ABC):
    def __init__(self, speed, xMin, xMax, yMin, yMax):
        super().__init__()
        self.__speed = speed
        self.__xMin, self.__xMax = xMin, xMax
        self.__yMin, self.__yMax = yMin, yMax

    def out_of_bounds(self):
        x, y = self.position()
        return x < self.__xMin or x > self.__xMax or y < self.__yMin or y > self.__yMax

    def get_speed(self):
        return self.__speed

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def move(self):
        pass

# Drone Class
class Drone(BoundedTurtle):
    drone_list = []

    @staticmethod
    def get_drones():
        return [drone for drone in Drone.drone_list if drone.__alive]

    def __init__(self, speed, xMin, xMax, yMin, yMax):
        super().__init__(speed, xMin, xMax, yMin, yMax)
        self.__initialize_drone(xMin, xMax, yMax)
        Drone.drone_list.append(self)
        self.__alive = True
        self.getscreen().ontimer(self.move, 200)

    def __initialize_drone(self, xMin, xMax, yMax):
        self.getscreen().tracer(0)
        self.up()
        self.__load_shape()
        self.goto(random.randint(xMin + 20, xMax - 20), yMax - 20)
        self.setheading(random.randint(250, 290))
        self.getscreen().tracer(1)

    def __load_shape(self):
        if 'Drone.gif' not in self.getscreen().getshapes():
            self.getscreen().addshape('Drone.gif')
        self.shape('Drone.gif')

    def move(self):
        self.forward(self.get_speed())
        if self.out_of_bounds():
            DroneInvasion.update_score(-5)
            self.remove()
        else:
            self.getscreen().ontimer(self.move, 200)

    def remove(self):
        self.__alive = False
        self.hideturtle()

# Bomb Class
class Bomb(BoundedTurtle):
    def __init__(self, init_heading, speed, xMin, xMax, yMin, yMax):
        super().__init__(speed, xMin, xMax, yMin, yMax)
        self.__initialize_bomb(init_heading)
        self.getscreen().ontimer(self.move, 100)

    def __initialize_bomb(self, init_heading):
        self.resizemode('user')
        self.color('red', 'red')
        self.shape('circle')
        self.turtlesize(0.25)
        self.setheading(init_heading)
        self.up()

    def move(self):
        self.forward(self.get_speed())
        if self.__check_collision() or self.out_of_bounds():
            self.remove()
        else:
            self.getscreen().ontimer(self.move, 100)

    def __check_collision(self):
        for drone in Drone.get_drones():
            if self.distance(drone) < 10:
                drone.remove()
                DroneInvasion.update_score(5)
                return True
        return False

    def remove(self):
        self.hideturtle()

# DroneInvasion Class
class DroneInvasion:
    score = 0
    score_turtle = None

    def __init__(self, xMin, xMax, yMin, yMax):
        self.__xMin, self.__xMax = xMin, xMax
        self.__yMin, self.__yMax = yMin, yMax

    def play(self):
        self.__initialize_game()
        self.__main_window.listen()
        mainloop()

    def __initialize_game(self):
        self.__main_window = LaserCannon(self.__xMin, self.__xMax, self.__yMin, self.__yMax).getscreen()
        self.__configure_screen()
        DroneInvasion.__initialize_score_display(self.__xMin, self.__yMax)
        self.__main_window.ontimer(self.__add_drone, 1000)

    def __configure_screen(self):
        self.__main_window.bgcolor('light green')
        self.__main_window.setworldcoordinates(self.__xMin, self.__yMin, self.__xMax, self.__yMax)

    @staticmethod
    def __initialize_score_display(xMin, yMax):
        DroneInvasion.score_turtle = Turtle()
        DroneInvasion.score_turtle.hideturtle()
        DroneInvasion.score_turtle.up()
        DroneInvasion.score_turtle.goto(xMin + 10, yMax - 20)
        DroneInvasion.update_score(0)

    def __add_drone(self):
        if len(Drone.get_drones()) < 7:
            Drone(1, self.__xMin, self.__xMax, self.__yMin, self.__yMax)
        self.__main_window.ontimer(self.__add_drone, 1000)

    @staticmethod
    def update_score(points):
        DroneInvasion.score += points
        DroneInvasion.score_turtle.clear()
        DroneInvasion.score_turtle.write(f"Score: {DroneInvasion.score}", font=("Arial", 16, "bold"))

# Main Function
def main():
    xMin, xMax, yMin, yMax = -200, 200, -200, 200
    game = DroneInvasion(xMin, xMax, yMin, yMax)
    game.play()

if __name__ == "__main__":
    main()
