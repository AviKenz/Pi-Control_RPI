#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO

# my import
import RpiInterpreterLib as Lib
import PwmHandler

# get script params
args = sys.argv
argsLen = len(args)

# avoid GPIO warnings
GPIO.setwarnings(False)
	
# get value of key in paramter passed to the py script
def get(key, isRequired = False, isNumber = True):
	Lib.log("d", "get({})".format(key))
	i = 0
	find = False
	val = ""
	for pair in args:
		if(pair.find(key) != -1):
			find = True
			val = pair.split("=")[1]
			if( isNumber ):
				val = int(val)
	if(find == False):
		Lib.log("w", "value of {} not found".format(key))
		if( isRequired ):
			Lib.log("e", "required value {} not found; PROGRAMM WILL TERMINATE".format(key))
			sys.exit()
	else:
		Lib.log("d", "key: {} - value: {}".format(key, val))
	return val	
									
# handle params passed to .py script an decide the action to take
def handleParam():
	Lib.log("d", "handleParam()")
	Lib.log("t", "print script param hier")
	direction = get("direction", True)
	if(direction == GPIO.OUT):
		mode = get("mode", True)
		pinNr = get("pin_number", True)
		GPIO.setmode(mode)
		GPIO.setup(pinNr, GPIO.OUT)
		signalTyp = get("signal_type", True)
		if(signalTyp == Lib.SIG_TYP_DC):
			state = get("state")
			interval = get("interval")
			nbrOfCycles = get("number_of_cycles")
			Lib.handleDcOutput(pinNr, state, interval, nbrOfCycles)
		elif(signalTyp == Lib.SIG_TYP_PWM):
			Lib.log("t", "implementing GPIO-OUTPUT-PWM... !")
			Lib.log("d", "channel = pin_number = {}".format(pinNr))
			ch = pinNr
			freq = get("freq", True)
			dc = get("duty_cycle")
			Lib.handlePwmOutput(pinNr, ch, freq, dc)
		else:
			Lib.log("e", "wrong SIGNAL TYP: {}; PROGRAMM WILL TERMINATE".format(signalTyp))
	elif(direction == GPIO.IN):
		Lib.log("t", "implement GPIO-INPUT... END")
	else:
		Lib.log("e", "direction: {} is wrong; PROGRAMM WILL TERMINATE!".format(direction))	

# start of programm
if __name__ == "__main__":
	Lib.log("d", "__main__")
	handleParam()
