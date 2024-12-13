import turtle

class Etch:
    def __init__(self):
        self.__myT = turtle.Turtle()
        self.__myScreen = turtle.Screen()
        self.__myT.color('blue')
        self.__myT.pensize(2)
        self.__myT.speed(0)
        self.__distance = 5
        self.__turn = 10
        self.__myScreen.onkey(self.fwd, "Up")
        self.__myScreen.onkey(self.bkwd, "Down")
        self.__myScreen.onkey(self.left, "Left")
        self.__myScreen.onkey(self.right, "Right")
        self.__myScreen.onkey(self.quit, "q")
        self.__myScreen.listen()

    def fwd(self):
        self.__myT.forward(self.__distance)

    def bkwd(self):
        self.__myT.backward(self.__distance)

    def left(self):
        self.__myT.left(self.__turn)

    def right(self):
        self.__myT.right(self.__turn)

    def quit(self):
        self.__myScreen.bye()

    def main(self):
        turtle.mainloop()
