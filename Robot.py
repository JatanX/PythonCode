import cv2
import sys
import os
from Enums import *
from Engines import *
from Sensors import *
from Sign import *
import threading
import time

class Robot:
    def __init__(self, name, error):
        self.name = name
        self.error = error
        self.ELeft = Engine(1)
        self.ERight = Engine(0)
        self.Camera = Camera(0)
        self.Degree = Degree(1)
        self.images = []
        self.images.append(Sign(PriorityEnum.MoBa, "images/move_backward.png"))
        self.images.append(Sign(PriorityEnum.MoFo, "images/move_forward.png"))
        self.images.append(Sign(PriorityEnum.StLe, "images/Steer_left.png"))
        self.images.append(Sign(PriorityEnum.StRi, "images/Steer_right.png"))
        self.images.append(Sign(PriorityEnum.TuLe, "images/turn_left.png"))
        self.images.append(Sign(PriorityEnum.TuRi, "images/turn_right.png"))
        img = cv2.imread(self.images[0].url)
        # self.Move(EngineDirection.Forward, EngineDirection.Backward, EngineIntensity.Speed1, EngineIntensity.Speed2)

    def run(self):
        time.sleep(2)
        print("Thread says Hi")

    def start(self):
        var = self.Camera.get()
        self.ELeft.Move(EngineDirection.Forward, EngineIntensity.Speed9)
        self.ERight.Move(EngineDirection.Forward, EngineIntensity.Speed9)
        self.Analyse("item")

        t=threading.Thread(target=self.run)
        #t.daemon = False  # set thread to daemon ('ok' won't be printed in this case)
        t.start()
        while(True):
            time.sleep(1)
            print("This is main")
        self.Stop()
        return







        #alle code die uitgevoert moet gaan worden

    def Move(self, DLeft, DRight, ILeft, IRight):
        self.ELeft.Move(DLeft, ILeft)
        self.ERight.Move(DRight, IRight)
        return

    def Stop(self):
        self.ELeft.Stop()
        self.ERight.Stop()

    def Execute(self, i):
        if(i is SignID.Stop.value):
            print("STOPPING")

    def Analyse(self, image):
        for item in self.images:
            print(item.url)
        print("Scanning")
