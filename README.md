This repository contains support for writing Python programs to serve sockets over Bluetooth.  The code derives from
the term projects of four students in Washington and Lee's Spring 2018 course
[CSCI 251: Android App Development](http://home.wlu.edu/~levys/courses/csci251s2018/).  The students originally
wrote code to support controlling a servo on a RaspberryPi, with the control signal coming from a simple Android
app.  Eventually I was able to factor this Python code into an abstract Python
[class](https://github.com/simondlevy/PythonBluetoothServer/blob/master/bluetooth_server.py), with the
servo code implemented as a 
[sub-class](https://github.com/simondlevy/PythonBluetoothServer/blob/master/servo_server.py).  

As a simple protocol, the server uses text messages delimited by a period ('.' character).   For those without a Raspberry Pi or servo, a simple &ldquo;call and response&rdquo; 
[example](https://github.com/simondlevy/PythonBluetoothServer/blob/master/lowhigh_server.py) 
allows you to try out the code on an ordinary computer: your client sends period-delimited
messages containing strings representing the values 0 through 100 ('0.', '1.',
'2.', ..., '99.', '100.'), and the server sends back 'LOW.' for values below 50,
and 'HIGH.' for values above.  

I have tested this code on the following two platforms:

* RaspberryPi 3 (servo example and call-and-response example)
* Sony VAIO Pro running Ubuntu 14.04 (call-and-response example)

## Setup

On a laptop or other ordinary computer with a bluetooth adapter, all you should need to do to before running the
examples is install the <b>pybluez</b> package:

<pre>
% sudo apt install python-bluez
</pre>

The setup on Raspberry Pi 3 is more complicated:

1. Edit <b>/lib/systemd/system/bluetooth.service</b> and add '-C' after 'bluetoothd'

2. Reboot

3. Run the command <tt>sudo sdptool add SP</b>

4. Run the command <tt>sudo apt-get install libbluetooth-dev</tt>

5. Run the command <tt>sudo apt-get install python3-dev</tt>

6. Run the command <tt>sudo pip3 install pybluez</tt>

On Raspberry Pi 3 we also found it necessary to run the server code as root; for example:

<pre>
% sudo python3 lowhigh_server.py`
</pre>

## Android app

The easiest way to try out this code is with the [Android client app](https://github.com/simondlevy/BluetoothClient)
that we developed to work with it.  This app uses the same simple protocol as the Python server, and has been
tested with the servo and call-and-response examples.
