#!/usr/bin/python

import sys
import os
import time
import RPi.GPIO as GPIO
import PiControlLib as AppLib

import time
from daemon import runner

# avoid GPIO warnings
GPIO.setwarnings(False)

# constant
SIG_TYP_DC = 0
SIG_TYP_PWM = 1


# output HIGH or LOW to choosen GPIO
def outputState(pinNr, state, release = False):
	AppLib.log("d", "outputState({}, {})".format(pinNr, state))
	GPIO.output(pinNr, state)
	if(state == GPIO.LOW and release):
		releaseGPIO(pinNr)

# free GPIO ressources
def releaseGPIO(pinNr):
	AppLib.log("d", "releaseGPIO({})".format(pinNr))
	GPIO.output(pinNr, GPIO.LOW)
	GPIO.cleanup()

# output 1 and 0 once to choosen GPIO port; CTRL + C abort the process
def blinkOnce(pinNr, interval):
	try:
		outputState(pinNr, GPIO.HIGH)
		time.sleep(interval)
		outputState(pinNr, GPIO.LOW)
		time.sleep(interval)
	except KeyboardInterrupt:
		AppLib.log("d", "Programm Interrupted with CTRL + C")
		releaseGPIO(pinNr)

# alternate state on GPIO a couple of times(nbrOfCycles) in some interval of time(interval in s);	
def blink(pinNr, interval, nbrOfCycles):
	AppLib.log("d", "blink({}, {})".format(pinNr, interval))
	if(nbrOfCycles == 0):
		while(True):
			blinkOnce(pinNr, interval)
	else:
		n = nbrOfCycles
		i = 0
		while(i < n):
			blinkOnce(pinNr, interval)
			i += 1
		releaseGPIO(pinNr)

# globally handle signal output on GPIO
def handleDcOutput(pinNr, state, interval, nbrOfCycles):
	AppLib.log("d", "handleDcOutput({}, {}, {}, {})".format(pinNr, state, interval, nbrOfCycles))	
	if(interval == 0 or interval == ""):
		# make sure to release the GPIO when state is GPIO.LOW
		outputState(pinNr, state, True)
	else:
		blink(pinNr, interval, nbrOfCycles)

def handlePwmOutput(ch, freq, dc):
	AppLib.log("d", "handlePwmOutput({}, {}, {})".format(ch, freq, dc))		
	

									
# handle params passed to .py script an decide the action to take
def handleParam():
	AppLib.log("e", "handleParam()")
	AppLib.log("t", "print script param hier")
	direction = AppLib.get("direction", True)
	if(direction == GPIO.OUT):
		mode = AppLib.get("mode", True)
		pinNr = AppLib.get("pin_number", True)
		GPIO.setmode(mode)
		GPIO.setup(pinNr, GPIO.OUT)
		signalTyp = AppLib.get("signal_type", True)
		if(signalTyp == SIG_TYP_DC):
			state = AppLib.get("state")
			interval = AppLib.get("interval")
			nbrOfCycles = AppLib.get("number_of_cycles")
			handleDcOutput(pinNr, state, interval, nbrOfCycles)
		elif(signalTyp == SIG_TYP_PWM):
			AppLib.log("t", "implementing GPIO-OUTPUT-PWM... !")
			AppLib.log("d", "channel = pin_number = {}".format(pinNr))
			ch = pinNr
			freq = AppLib.get("freq", True)
			dc = AppLib.get("duty_cycle")
			#action is needed by the daemon runner in PwmDaemon; value: start|stop|restart
			action = "start"
			if (dc == 0):
				action = "stop"
			AppLib.log("d", "running PwmDaemon: python /usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format(action, ch, freq, dc))
			os.system("python /usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format(action, ch, freq, dc))
			#execfile("/usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format("start", ch, freq, dc))			
		else:
			AppLib.log("e", "wrong SIGNAL TYP: {}; PROGRAMM WILL TERMINATE".format(signalTyp))
	elif(direction == GPIO.IN):
		AppLib.log("t", "implement GPIO-INPUT... END")
	else:
		AppLib.log("e", "direction: {} is wrong; PROGRAMM WILL TERMINATE!".format(direction))	

# start of programm
if __name__ == "__main__":
	AppLib.log("d", "__main__")
	handleParam()
