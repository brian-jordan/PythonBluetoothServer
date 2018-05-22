#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from bluetooth_server import BluetoothServer

class LowHighServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)

    def handleMessage(self, message):

        self.send('LOW' if int(message) < 50 else 'HIGH')

if __name__ == '__main__':

    server = LowHighServer()

    server.start()
