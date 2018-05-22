#!/usr/bin/python3
'''
Serves a Bluetooth socket 

MUST BE RUN AS ROOT (USE SUDO)
'''

BUFSIZE = 1024

import os

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

            # Track strings delimited by '.'
            s = ''

            while True:

                c = client_sock.recv(1).decode('utf-8')

                if c == '.' and len(s) > 0:
                    value = int(s)
                    print(value)
                    s = ''
                    client_sock.send((('LOW' if value < 50 else 'HIGH') + '.').encode('utf-8'))
                else:
                    s += c

        except IOError:
            pass

        except KeyboardInterrupt:

            if client_sock is not None:
                client_sock.close()

            server_sock.close()

            print("Server going down")
            break

main()
