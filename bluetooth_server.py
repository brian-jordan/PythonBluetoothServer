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

            while True:

                b = client_sock.recv(1)

                print(b.decode('utf-8'))

                continue

                if len(data) > 0:  # avoid reporting empty messages (not sure why we get them!)

                    value = int(data.decode('utf-8'))

                    print(value)

                    client_sock.send((('LOW' if value < 5 else 'HIGH') + '.').encode('utf-8'))

        except IOError:
            pass

        except KeyboardInterrupt:

            if client_sock is not None:
                client_sock.close()

            server_sock.close()

            print("Server going down")
            break

main()
