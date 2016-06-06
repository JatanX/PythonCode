import serial

class Engine:
    def __init__(self, isleft):
        self.isleft = isleft
        try:
            self.port = serial.Serial(
            "/dev/serial/by-id/usb-Microchip_Technology_Inc._MCP2200_USB_Serial_Port_Emulator_0000995030-if00",
    	   2400,
    	   serial.EIGHTBITS,
    	   serial.PARITY_NONE,
    	   serial.STOPBITS_ONE
           )
        except Exception as e:
            #print("Port not found\n")
            return
        return

    def Move(self, Direction, Intensity):
        send = 0b10000000
        send = (send | (self.isleft << 6))
        send = (send | (Direction << 5))
        send = (send | (1 << 4))
        send = (send | Intensity)
        var = chr(send)
        try:
            self.port.write(var + "\n")
        except Exception as e:
            #print("port not found\n")
            return

    def Stop(self):
        send = 0b10100000
        send = (send | (self.isleft << 6))
        var = chr(send)
        #print("stopping")
        try:
            self.port.write(var + "\n")
        except Exception as e:
            print("port not found\n")
            return
