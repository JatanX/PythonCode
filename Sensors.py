import os
from picamera.array import PiRGBArray
import picamera
from picamera import PiCamera
import serial
import smbus
import cv2
import time
import numpy as np

class Sensor:
    def __init__(self):
        return
    def get(self):
        print("This function is abstract")

class Degree(Sensor):
    def __init__(self, id):
        self.id = id
        self.bus = smbus.SMBus(1) #1 = /dev/i2c-1 which is the port used by the L3GD20H Gyro.
	    #DEVICE_ADDRESS = 0b1101011
        self.DEVICE_ADDRESS = 0x6B
        self.CTRL1 = 0x20
        self.OUT_X_L = 0X28
        self.OUT_X_H = 0X29
        self.OUT_Y_L = 0X2A
        self.OUT_Y_H = 0X2B
        self.OUT_Z_L = 0x2C
        self.OUT_Z_H = 0x2D

    def power_on(self):
        self.bus.write_byte_data(self.DEVICE_ADDRESS, self.CTRL1, 0b00001111)
    def power_off(self):
        self.bus.write_byte_data(self.DEVICE_ADDRESS, self.CTRL1, 0b00000111)

    def get(self):
        #z_val_l=bus.read_byte_data(DEVICE_ADDRESS,OUT_Z_L)
        z_val_h=self.bus.read_byte_data(self.DEVICE_ADDRESS,self.OUT_Z_H)
        #z_val = (z_val_h << 8) | z_val_l
        #z_val = z_val >> 8
        z_val = z_val_h * 360
        z_val = z_val / 255
        z_val = 360 - z_val
        if z_val > 180:
            z_val -= 360
        return z_val

class Camera(Sensor):
    def __init__(self, id):
        self.id = id

    def get(self):
        try:
            os.system("rm images/capture.png")
            camera = picamera.PiCamera()
            camera.resolution = (1280, 720)
            camera.capture("images/capture.png")
            camera.close()
            time.sleep(1)
        except Exception as e:
            print(e)
