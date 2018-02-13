#!/usr/bin/python

import sys
import RPi.GPIO as GPIO
import datetime
import time

# constants; define name of control in android App
SWITCH_CONTROL_NAME = "SwitchControl"
BUTTON_CONTROL_NAME = "ButtonControl"
PWM_CONTROL_NAME = "PwmControl"
BLINK_CONTROL_NAME = "BlinkControl"

# get script parameters
args = sys.argv

#constants
KEY_NAME = "name"
KEY_MODE = "mode"
KEY_PIN_NUMBER = "pin_number"
KEY_DIRECTION = "direction"
KEY_STATE = "state"
KEY_INTERVAL = "interval"
KEY_NUMBER_OF_CYCLES = "number_of_cycles"
KEY_SIGNAL_TYPE = "signal_typ"

def log(code, message):
	now = datetime.datetime.now()
	now = now.strftime("%Y-%m-%d %H:%M:%S")
	clName = ""
	result = "";
	if(code == "e"):
		clName = 'interpreter error'
	elif(code == "w"):
		clName = 'interpreter warn'
	elif(code == "i"):
		clName = 'interpreter info'
	elif(code == "d"):
		clName = 'interpreter debug'
	elif(code == "t"):
		clName = 'interpreter todo'
	else:
		clName = 'interpreter noname'
	result = "<p class=" + clName + ">" + now + " " + message + "</p>"
	print result
	
# get value of key in paramter passed to the py script
def get(key, isRequired = False, isString = False):
	log("d", "get({})".format(key))
	i = 0
	find = False
	val = ""
	for pair in args:
		if(pair.find(key) != -1):
			find = True
			val = pair.split("=")[1]
			if( isString ):
				val = str(val)
			else:
				val = int(val)
	if(find == False):
		log("w", "value of '{}' not found".format(key))
		if( isRequired ):
			log("e", "required value '{}' not found; PROGRAMM WILL TERMINATE".format(key))
			sys.exit()
	else:
		log("d", "key: '{}' - value: '{}'".format(key, val))
	return val

def getName():
	return get(KEY_NAME, True, True)

def handleSwitchControl():
	GPIO.setmode(get(KEY_MODE, True))
	pinNr = get(KEY_PIN_NUMBER, True)
	GPIO.setup(pinNr, GPIO.OUT)
	state = get(KEY_STATE, True)
	GPIO.output(pinNr, state)
	if(state == GPIO.LOW):
		GPIO.cleanup()
		log("d", "Port {} cleaned".format(pinNr))

def handleButtonControl():
	GPIO.setmode(get(KEY_MODE, True))
	pin = get(KEY_PIN_NUMBER, True)
	GPIO.setup(pin, GPIO.OUT)
	state = get(KEY_STATE, True)
	GPIO.output(pin, state)
	if(state == GPIO.LOW):
		GPIO.cleanup()
		log("d", "Port {} cleaned".format(pin))

def handleBlinkControl():
	GPIO.setmode(get(KEY_MODE, True))
	pin = get(KEY_PIN_NUMBER, True)
	GPIO.setup(pin, GPIO.OUT)
	interval = get(KEY_INTERVAL)
	nrOfCycles = get(KEY_NUMBER_OF_CYCLES, True)
	if(nrOfCycles == 0):	
		try:
			while(True):
				GPIO.output(pin, GPIO.HIGH)
				time.sleep(interval)
				GPIO.output(pin, GPIO.LOW)
				time.sleep(interval)
		except KeyboardInterrupt:
			GPIO.output(pin, GPIO.LOW)
			GPIO.cleanup()
			log("d", "Programm Interrupted with CTRL + C")
	else:	
		try:
			counter = 0
			while(counter < nrOfCycles):
				GPIO.output(pin, GPIO.HIGH)
				time.sleep(interval)
				GPIO.output(pin, GPIO.LOW)
				time.sleep(interval)
				counter += 1
		except KeyboardInterrupt:
			GPIO.output(pin, GPIO.LOW)
			GPIO.cleanup()
			log("d", "Programm Interrupted with CTRL + C")

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
	
