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
'2.', ..., '99.', '100.'), and the server sends back 'LOW' for values below 50,
and 'HIGH' for values above.  I have tested this code on the following two
platforms:

* RaspberryPi 3 (servo example and call-and-response example)
* Sony VAIO Pro running Ubuntu 14.04 (call-and-response example)
