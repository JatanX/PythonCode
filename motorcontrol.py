#!/usr/bin/python

import serial

port = serial.Serial(
	"/dev/serial/by-id/usb-Microchip_Technology_Inc._MCP2200_USB_Serial_Port_Emulator_0000995030-if00",
	2400,
	serial.EIGHTBITS,
	serial.PARITY_NONE,
	serial.STOPBITS_ONE
	)

while True:
	user_input = raw_input("Give me a command: ")
	if user_input == "w":
		data = bytearray([0b10111111])
		port.write(data +'\n')
		data = bytearray([0b11111111])
		port.write(data +'\n')

	if user_input == "s":
		data = bytearray([0b10011111])
		port.write(data +'\n')
		data = bytearray([0b11011111])
		port.write(data +'\n')

	if user_input == "a":
		data = bytearray([0b10111111])
		port.write(data +'\n')
		data = bytearray([0b11011111])
		port.write(data +'\n')

	if user_input == "d":
		data = bytearray([0b10011111])
		port.write(data +'\n')
		data = bytearray([0b11111111])
		port.write(data +'\n')

	if user_input == "p":
		data = bytearray([0b11000000])
		data2 = bytearray([0b10000000])
		port.write(data +'\n')
		port.write(data2 +'\n')
		break
port.close()
