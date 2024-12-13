from threading import Thread
import time

class EventHandler(Thread):   #inherits from Thread class
    def __init__(self):
        super().__init__()
        self.__queue = []
        self.__eventKeeper = {}

    def addEvent(self, eventName):
        self.__queue.append(eventName)

    def registerCallback(self, event, func):
        self.__eventKeeper[event] = func

    def run(self):            #start calls this method
        while (True):
            if len(self.__queue) > 0:
                nextEvent = self.__queue.pop(0)
                callBack = self.__eventKeeper[nextEvent]
                callBack()     #call registered function for event
            else:
                time.sleep(1)  #pause for 1 second 

def myMouse():
    print('Oh no, the mouse was clicked!')

def myKey():
    print('A key has been pressed.')


