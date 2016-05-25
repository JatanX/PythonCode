import os
#import cv2
import numpy

class Sensor:
    def __init__(self):
        return
    def get(self):
        print("This function is abstract")
        return

class Degree(Sensor):
    def __init__(self, id):
        self.id = id
        return

    def get(self):
        return 90

class Camera(Sensor):
    def __init__(self, id):
        self.id = id
        return

    def get(self):
        try:
            os.system('raspistill -o image.jpg')
        except Exception as e:
            print("\n")
        return ('image.jpg')
