import time
from threading import Thread

class threadManager:
    def __init__(self, func, getQueueSize=None):
        self.killFlag = False
        self.func = func
        self.getQueueSize = getQueueSize
        thread = Thread(target = self.loop)
        thread.start()

    def loop(self):
        """Single thread that sets killFlag for both the filewriter and directoryHandler to True, if
        it wakes and flag has not been reset, meaning no data has been processed it kills all threads"""
        while not self.killFlag:
            if self.getQueueSize:
                print("Queue Size: ", self.getQueueSize())
            self.killFlag = True
            time.sleep(300)  # Sleeping for some amount of time to allow threads to reset flag if they are still processing data
        self.func()  # Calling function that kills the currently running threads

    def resetFlag(self):
        """Function to allow threads access to resetting flag"""
        self.killFlag = False