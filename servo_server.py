#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages for running a servo motor on Raspberry Pi.

Copyright 2018  Emily Boyes, Gunnar Bowman, Trip Calihan, Simon D. Levy, Sheperd Sims

MIT License
'''

from bluetooth_server import BluetoothServer
import RPi.GPIO as GPIO

class ServoServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(11,GPIO.OUT)

        pwm = GPIO.PWM(11, 50)
        pwm.start(5)

    def handleMessage(self, message):

        # Convert [0,100] => [1,11]
        duty = float(data)/10 + 1

        # Don't know why we need this!
        if duty >= 1 and duty <= 11:
            pwm.ChangeDutyCycle(duty)


if __name__ == '__main__':

    server = ServoServer()

    server.start()
