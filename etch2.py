from turtle import Turtle, mainloop

class Etch(Turtle):
    def __init__(self):
        super().__init__()
        self.__screen = self.getscreen()
        self.color('blue')
        self.pensize(2)
        self.speed(0)
        self.__distance = 5
        self.__turn = 10
        self.__screen.onkey(self.fwd, "Up")
        self.__screen.onkey(self.bkwd, "Down")
        self.__screen.onkey(self.left10, "Left")
        self.__screen.onkey(self.right10, "Right")
        self.__screen.onkey(self.quit, "q")
        self.__screen.listen()       
        self.main()

    def fwd(self):
        self.forward(self.__distance)

    def bkwd(self):
        self.backward(self.__distance)

    def left10(self):
        self.left(self.__turn)

    def right10(self):
        self.right(self.__turn)

    def quit(self):
        self.__screen.bye()

    def main(self):
        mainloop()

if __name__ == '__main__':
    etch = Etch()

