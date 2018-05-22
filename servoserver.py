#!/usr/bin/python
'''
Serves a Bluetooth socket for running a servo on the Raspberry Pi

MUST BE RUN AS ROOT (USE SUDO)
'''

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)

pwm = GPIO.PWM(11, 50)
pwm.start(5)

import logging
import logging.handlers
import argparse
import sys
import os
import time

import bluetooth as bt

# Main loop
def main():

    # Make device visible
    os.system("hciconfig hci0 piscan")

    # Create a new server socket using RFCOMM protocol
    server_sock = bt.BluetoothSocket(bt.RFCOMM)

    # Bind to any port
    server_sock.bind(("", bt.PORT_ANY))

    # Start listening
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # The service UUID to advertise
    uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

    # Start advertising the service
    bt.advertise_service(server_sock, "RaspiBtSrv",
                       service_id=uuid,
                       service_classes=[uuid, bt.SERIAL_PORT_CLASS],
                       profiles=[bt.SERIAL_PORT_PROFILE])

    # Outer loop: listen for connections from client
    while True:

        print("Waiting for connection on RFCOMM channel %d" % port)

        try:

            client_sock = None

            # This will block until we get a new connection
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from " +  str(client_info))

            while True:

		    data = client_sock.recv(1024).rstrip() # remove linefeed, carriage-return

                    if len(data) > 0:  # avoid reporting empty messages (not sure why we get them!)

                        # Convert [0,100] => [1,11]
			duty = float(data)/10 + 1

                        # Don't know why we need this!
                        if duty >= 1 and duty <= 11:
    			    pwm.ChangeDutyCycle(duty)

        except IOError:
            pass

        except KeyboardInterrupt:

            if client_sock is not None:
                client_sock.close()

            server_sock.close()

            print("Server going down")
            break

    pwm.stop()

main()
