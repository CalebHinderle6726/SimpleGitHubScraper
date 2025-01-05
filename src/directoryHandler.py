import requests
import threading
import threadManager
import time
from threading import Thread

class directoryHandler:
    def __init__(self, filewriter):
        self.dirs = []
        self.exit = False
        self.startThreads()
        self.threadManager = threadManager.threadManager(self.killThreads)
        self.filewriter = filewriter

    def addDir(self, dir):
        self.dirs.append(dir)

    def killThreads(self):
        self.exit = True

    def startThreads(self):
        numThreads = 20
        for _ in range(numThreads):
            thread = Thread(target = self.handleDirs, args = (self.dirs, lambda:self.exit,))
            thread.start()

    def handleDirs(self, dirs, exit):
        """Keeps threads looping while there are directories in dirs list or the threads have not been told
        to stop by the threadManager"""
        while not exit() or dirs:
            if dirs:
                [direc, branch] = dirs.pop()
                self.parseFilesFolders(direc, dirs, branch)
            else:
                time.sleep(1)  # Sleeping when there are no directories to process to save resources
        print("Thread: ", threading.currentThread().getName(), " quitting")

    def parseFilesFolders(self, url, dirs, branch):
        """Initial page parsing from basic GitHub url, adding files to shared file list and
        directories to shared directory list"""
        base = url.split("/tree/", 1)[0]
        headers = {'Accept': 'application/json'}  # Auth token can be added here to increase limit on number of repos
        fileUrlPrefix = base.replace("https://github.com", "") + "/blob/" + branch + "/"
        r = requests.get(url, headers=headers)  # Making reguest to get contents of directory popped from shared list
        try:
            treeItems = r.json().get("payload").get("tree").get("items")  # Grabbing items from the current directory page
            for treeItem in treeItems:
                itemContentType = treeItem.get("contentType")
                itemPath = treeItem.get("path")
                self.filewriter.threadManager.resetFlag()  # Resetting filewriter timeout flag as there are still files to process
                if itemContentType == "file":
                    self.filewriter.addFile(fileUrlPrefix + itemPath)  # Adding file to shared file list in the filewriter class
                elif itemContentType == "directory":
                    self.threadManager.resetFlag()  # Resetting directory handler timeout flag as there are still directories to process
                    dirs.append([base + "/tree/" + branch + "/" + itemPath + "?noancestors=1", branch])  # Adding directory urls and branch to shared list
        except Exception as e:
            print(url)
            print(e)
            
        




