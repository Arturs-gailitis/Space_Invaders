class EventHandler:
    def __init__(self):
        self.__queue = []          #holds events
        self.__eventKeeper = {}    #dict of event types and callbacks

    def addEvent(self, eventName):
        self.__queue.append(eventName)

    #specify function to call when event occurs
    def registerCallback(self, event, func):
        self.__eventKeeper[event] = func

    def run(self):
        while (True):    #endless loop
            if len(self.__queue) > 0:
                nextEvent = self.__queue.pop(0) #get next event
                self.__eventKeeper[nextEvent]() #run callback function
            else:
                print('queue is empty')

def myMouse():
    print('Oh no, the mouse was clicked!')

def myKey():
    print('A key has been pressed.')

def runEventHandler():
    eh = EventHandler()
    eh.registerCallback('key', myKey)
    eh.registerCallback('mouse', myMouse)
    eh.addEvent('mouse')
    eh.addEvent('key')
    eh.addEvent('mouse')
    eh.run()

