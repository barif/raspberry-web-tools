#! /usr/bin/env python

# Read the output of an Arduino which may be printing sensor output,
# and at the same time, monitor the user's input and send it to the Arduino.
# See also
# http://www.arcfn.com/2009/06/arduino-sheevaplug-cool-hardware.html

import sys, serial, select

class Arduino() :
    def run(self, baud=9600) :
        # Port may vary, so look for it:
        baseports = ['/dev/ttyUSB', '/dev/ttyACM', '/dev/ttyACM0']
        self.ser = None
        for baseport in baseports :
            if self.ser : break
            for i in xrange(0, 8) :
                try :
                    port = baseport + str(i)
                    self.ser = serial.Serial(port, baud, timeout=1)
                    print "Opened", port
                    break
                except :
                    self.ser = None
                    pass

        if not self.ser :
            print "Couldn't open a serial port"
            sys.exit(1)

        self.ser.flushInput()
        while True :
            # Check whether the user has typed anything (timeout of .2 sec):
            inp, outp, err = select.select([sys.stdin, self.ser], [], [], 2)

            # If the user has typed anything, send it to the Arduino:
            if sys.stdin in inp :
                line = sys.stdin.readline()
                self.ser.write(line)

            # If the Arduino has printed anything, display it:
            if self.ser in inp :
                line = self.ser.readline().strip()
                print "Arduino:", line

arduino = Arduino()
try :
    if len(sys.argv) > 1 :
        print "Using", sys.argv[1], "baud"
        arduino.run(baud=sys.argv[1])
    else :
        arduino.run()
except serial.SerialException :
    print "Disconnected (Serial exception)"
except IOError :
    print "Disconnected (I/O Error)"
except KeyboardInterrupt :
    print "Interrupt"