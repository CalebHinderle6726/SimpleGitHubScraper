import os
import requests
import threading
import time
import timeit
import threadManager
from requests.exceptions import ChunkedEncodingError
from threading import Thread

class filewriter:
    def __init__(self):
        self.files = []
        self.exit = False
        self.whitelist = ['cs', 'py', 'java', 'c']
        self.startThreads()
        self.threadManager = threadManager.threadManager(self.killThreads, self.getFileCount)
        self.time = timeit.default_timer()
        self.count = 0
        self.end = 0

    def addFile(self, file):
        self.files.append(file)
    
    def getFileCount(self):
        return len(self.files)

    def killThreads(self):
        self.exit = True
        print("Time: ", self.end - self.time)

    def startThreads(self):
        numThreads = 100
        for _ in range(numThreads):
            thread = Thread(target = self.handleFile, args = (self.files, lambda:self.exit,))
            thread.start()

    def handleFile(self, fileList, exit):
        """Keeps threads looping while there are files in files list or the threads have not been told
        to stop by the threadManager"""
        while not exit() or fileList:
            if fileList:
                url = fileList.pop()
                end = url.rsplit('.', 1)[-1]  # Getting the file type to use in specifying directory
                if end in self.whitelist:
                    self.threadManager.resetFlag()
                    url = "https://raw.githubusercontent.com" + url.replace("/blob/", "/refs/heads/")  # Getting url to raw file contents
                    r = requests.get(url, stream=True)  # Using get request to stream the contents of the file
                    self.count += 1
                    self.saveFile("data/" + end, r)  # Saving file contents to numbered file in file type labeled directory
                    self.end = timeit.default_timer()
            else:
                time.sleep(1)
        print("Thread: ", threading.currentThread().getName(), " quitting")


    def saveFile(self, filepath, fileDataStream):
        """Writing raw file contents to text files in file type specific directories"""
        filename = 'test'+ str(self.count) + '.txt'
        try:
            f = open(filepath + '/' + filename, 'wb')
        except FileNotFoundError:
            os.makedirs(filepath)
            f = open(filepath + '/' + filename, 'wb')
        try:
            for data in fileDataStream.iter_content(chunk_size=1024):  # Streaming to file in chunks to avoid ChunkedEncodingError
                f.write(data)
        except ChunkedEncodingError as e:
            print(f"Invalid chunk {str(e)}")
        f.close()


