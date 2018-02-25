#!/usr/bin/python

import sys
import os
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
KEY_FREQUENCY = "frequency"
KEY_DUTY_CYCLE = "duty_cycle"

def log(code, message):
	now = datetime.datetime.now()
	now = now.strftime("%Y-%m-%d %H:%M:%S")
	clName = ""
	result = "";
	if(code == "e"):
		clName = 'userapp error'
	elif(code == "w"):
		clName = 'userapp warn'
	elif(code == "i"):
		clName = 'userapp info'
	elif(code == "d"):
		clName = 'userapp debug'
	elif(code == "t"):
		clName = 'userapp todo'
	else:
		clName = 'usersoft noname'
	result = "<p class=\'" + clName + "\'>" + now + " " + message + "</p>"
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
			
def handlePwmControl():
	mode = get(KEY_MODE, True)
	pin = get(KEY_PIN_NUMBER, True)
	freq = get(KEY_FREQUENCY, True)
	dc = get(KEY_DUTY_CYCLE, True)
	# the action is for the pwm daemon; values: start|stop|restart
	action = "start"
	if(dc == 0):
		action = "stop"
	log("d", "call Script PwmDaemon.py: action: {} | channel: {} | frequency: {} | duty cycle: {}".format(action, pin, freq, dc))
	os.system("python /usr/lib/cgi-bin/PwmDaemon.py {} {} {} {} {}".format(action, mode, pin, freq, dc))
