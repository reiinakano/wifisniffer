import datetime
import time
import threading

class AddToList(threading.Thread):

    def __init__(self, lock, entryList):
        threading.Thread.__init__(self)
        self.totalAdded = 0
        self.entryList = entryList
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            self.entryList.append("AddToList at {}".format(datetime.datetime.now()))
            self.totalAdded += 1
            self.lock.release()
            print("totalAdded: {}".format(self.totalAdded))
            time.sleep(2)


class SaveList(threading.Thread):
    def __init__(self, lock, entryList):
        threading.Thread.__init__(self)
        self.totalSaved = 0
        self.entryList = entryList
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            self.totalSaved += len(self.entryList)
            del self.entryList[:]
            self.lock.release()
            print("totalSaved: {}".format(self.totalSaved))
            time.sleep(3)


if __name__=="__main__":
    lock=threading.Lock()
    entryList=[]

    addClass = AddToList(lock, entryList)
    addClass.start()

    saveClass = SaveList(lock, entryList)
    saveClass.start()