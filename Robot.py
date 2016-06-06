import cv2
import sys
import os
from Enums import *
from Engines import *
from Sensors import *
from Sign import *
from threading import *
from Queue import Queue
import time
import numpy as np
import Image
import pytesseract
import commands

class Robot:
    def __init__(self, name, error):
        self.name = name
        self.error = error
        self.ELeft = Engine(1)
        self.ERight = Engine(0)
        self.Camera = Camera(0)
        self.Degree = Degree(1)
        self.images = []
        self.lock = Lock()
        self.q = Queue()
        self.images.append(Sign(PriorityEnum.Exit, "Exit"))
        self.images.append(Sign(PriorityEnum.Stop, "Stop"))
        self.images.append(Sign(PriorityEnum.Left, "Left"))
        self.images.append(Sign(PriorityEnum.Right, "Right"))
        self.images.append(Sign(PriorityEnum.Backward, "Backward"))
        self.images.append(Sign(PriorityEnum.Forward, "Forward"))

    def start(self):
        while(True):
            #self.Camera.get()
            self.foundImages = self.Analyse()
            if not self.foundImages:
                pass
            else:
                for item in self.foundImages:
                    self.Execute(item)
        return

    def Move(self, DLeft, DRight, ILeft, IRight, Duration):
        self.ELeft.Move(DLeft, ILeft)
        self.ERight.Move(DRight, IRight)
        i = Duration
        while(i > 0):
            try:
                status = self.q.get()
                print("status is: " + status)
            except:
                print("still going")
                pass
            if status == "stop":
                break
            time.sleep(0.1)
            i -= 1
        return

    def Stop(self):
        self.ELeft.Stop()
        self.ERight.Stop()
        self.MakeAllThreadsExit()
        print("Stopping")

    def Exit(self):
        self.Stop()
        print("Exiting Program")
        sys.exit()
        #kan raar doen als aangeroepen in een thread
        #moet nog onderzocht worden

    def Execute(self, i):
        if(PriorityEnum.Exit == i):
            self.Exit()
        if(PriorityEnum.Stop == i):
            self.Stop()
        if(PriorityEnum.Backward == i):
            self.MoveDirection(EngineDirection.Backward, EngineIntensity.Speed6)
            print("move back")
        if(PriorityEnum.Forward == i):
            self.MoveDirection(EngineDirection.Forward, EngineIntensity.Speed6)
            print("move forward")
        if(PriorityEnum.Left == i):
            print("turn left")
            self.MakeTurn(EngineDirection.Backward, EngineDirection.Forward, EngineIntensity.Speed15, EngineIntensity.Speed15, -90)
        if(PriorityEnum.Right == i):
            print("turn right")
            self.MakeTurn(EngineDirection.Forward, EngineDirection.Backward, EngineIntensity.Speed15, EngineIntensity.Speed15, 90)
        self.Stop()
    

    def MoveDirection(self, Dir, Int):
        threadSign = Thread( target = self.StopExitCheck)
        threadSign.daemon = False
        threadSign.start()
        self.Move(Dir, Dir, Int, Int, 50)
        threadSign.join()

    def MakeTurn(self, DirLeft, DirRight, IntLeft, IntRight, AngleToCompare):
        threadgyro = Thread( target = self.turnTill, args=( AngleToCompare,))
        threadgyro.daemon = False
        self.Degree.power_on()
        threadgyro.start()
        self.Move(DirLeft, DirRight, IntLeft, IntRight, 50)
        threadgyro.join()
        self.Degree.power_off()

    def turnTill(self, compareval):
        count = 0
        degrees = 0
        t0  = time.clock()
        output = 0
        compareval = (compareval * 0.5)
        print("Zit in thread")
        while(True):
            time.sleep(0.1)
            temp = self.Degree.get()
            temp = temp * 0.1
            output += temp
            if (compareval > 0 and output >= compareval) or (compareval < 0 and output <= compareval):
                print("stopping now")
                self.Stop()
                self.MakeAllThreadsExit()
                return
            if self.q.empty:
                pass
            else:
                status = self.q.get()
                if status == "stop":
                    return

    def StopExitCheck(self):
        while(True):
            if self.q.empty:
                pass
            else:
                status = self.q.get()
                if status == "stop":
                    return
            list = self.Analyse()
            for item in list:
                if item == PriorityEnum.Stop:
                    self.Stop()
                    self.foundImages = None
                    return
                if item == PriorityEnum.Exit:
                    self.MakeAllThreadsExit()
                    self.Exit()

    def MakeAllThreadsExit(self):
        i = activeCount()
        while(i >= 0):
            self.q.put("stop")
            i -= 1

    def Analyse(self):
        retlist = []
        self.lock.acquire()
        self.Camera.get()
        gray = cv2.imread('images/capture.png',0)
        self.lock.release()

        ret,thresh = cv2.threshold(gray, 100 ,240, 0)
        cv2.imwrite("ThreshImage.png", thresh)
        print("Done taking pictures, scanning for text now")
        sentence = pytesseract.image_to_string(Image.open('ThreshImage.png'))
        print(sentence)
        for item in self.images:
            if item.Text in sentence:
                print("yes")
                retlist.append(item.SignID)
        retlist.append(0)
        retlist.sort()
        return retlist
