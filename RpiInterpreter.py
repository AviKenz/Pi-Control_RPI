#!/usr/bin/python

import sys
import os
import time
import RPi.GPIO as GPIO

import time
from daemon import runner

# avoid GPIO warnings
GPIO.setwarnings(False)

# constant
SIG_TYP_DC = 0
SIG_TYP_PWM = 1 

args = sys.argv
argsLen = len(args)

def log(code, message):
	result = "";
	if(code == "e"):
		result = "<p class='interpreter error'>" + message + "</p>"
	elif(code == "w"):
		result = "<p class='interpreter warn'>" + message + "</p>"
	elif(code == "i"):
		result = "<p class='interpreter info'>" + message + "</p>"
	elif(code == "d"):
		result = "<p class='interpreter debug'>" + message + "</p>"
	elif(code == "t"):
		result = "<p class='interpreter todo'>" + message + "</p>"
	else:
		result = "<p class='interpreter noname'>" + message + "</p>"
	print result
		
# get value of key in paramter passed to the py script
def get(key, isRequired = False, isNumber = True):
	log("d", "get({})".format(key))
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
		log("w", "value of {} not found".format(key))
		if( isRequired ):
			log("e", "required value {} not found; PROGRAMM WILL TERMINATE".format(key))
			sys.exit()
	else:
		log("d", "key: {} - value: {}".format(key, val))
	return val

# output HIGH or LOW to choosen GPIO
def outputState(pinNr, state, release = False):
	log("d", "outputState({}, {})".format(pinNr, state))
	GPIO.output(pinNr, state)
	if(state == GPIO.LOW and release):
		releaseGPIO(pinNr)

# free GPIO ressources
def releaseGPIO(pinNr):
	log("d", "releaseGPIO({})".format(pinNr))
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
		log("d", "Programm Interrupted with CTRL + C")
		releaseGPIO(pinNr)

# alternate state on GPIO a couple of times(nbrOfCycles) in some interval of time(interval in s);	
def blink(pinNr, interval, nbrOfCycles):
	log("d", "blink({}, {})".format(pinNr, interval))
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
	log("d", "handleDcOutput({}, {}, {}, {})".format(pinNr, state, interval, nbrOfCycles))	
	if(interval == 0 or interval == ""):
		# make sure to release the GPIO when state is GPIO.LOW
		outputState(pinNr, state, True)
	else:
		blink(pinNr, interval, nbrOfCycles)

def handlePwmOutput(ch, freq, dc):
	log("d", "handlePwmOutput({}, {}, {})".format(ch, freq, dc))		
	

									
# handle params passed to .py script an decide the action to take
def handleParam():
	log("e", "handleParam()")
	log("t", "print script param hier")
	direction = get("direction", True)
	if(direction == GPIO.OUT):
		mode = get("mode", True)
		pinNr = get("pin_number", True)
		GPIO.setmode(mode)
		GPIO.setup(pinNr, GPIO.OUT)
		signalTyp = get("signal_type", True)
		if(signalTyp == SIG_TYP_DC):
			state = get("state")
			interval = get("interval")
			nbrOfCycles = get("number_of_cycles")
			handleDcOutput(pinNr, state, interval, nbrOfCycles)
		elif(signalTyp == SIG_TYP_PWM):
			log("t", "implementing GPIO-OUTPUT-PWM... !")
			log("d", "channel = pin_number = {}".format(pinNr))
			ch = pinNr
			freq = get("freq", True)
			dc = get("duty_cycle")
			#action is needed by the daemon runner in PwmDaemon; value: start|stop|restart
			action = "start"
			if (dc == 0):
				action = "stop"
			log("d", "running PwmDaemon: python /usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format(action, ch, freq, dc))
			os.system("python /usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format(action, ch, freq, dc))
			#execfile("/usr/lib/cgi-bin/PwmDaemon.py {} {} {} {}".format("start", ch, freq, dc))			
		else:
			log("e", "wrong SIGNAL TYP: {}; PROGRAMM WILL TERMINATE".format(signalTyp))
	elif(direction == GPIO.IN):
		log("t", "implement GPIO-INPUT... END")
	else:
		log("e", "direction: {} is wrong; PROGRAMM WILL TERMINATE!".format(direction))	

# start of programm
if __name__ == "__main__":
	log("d", "__main__")
	handleParam()
