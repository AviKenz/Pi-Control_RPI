#!/usr/bin/python
import RPi.GPIO as GPIO

# constant
SIG_TYP_DC = 0
SIG_TYP_PWM = 1 

def log(code, message):
	if(code == "e"):
		print "[ERROR] " + message
	elif(code == "w"):
		print "[WARN] " + message
	elif(code == "i"):
		print "[INFO] " + message
	elif(code == "d"):
		print "[DEBUG] " + message
	elif(code == "t"):
		print "[TODO] " + message
	else:
		print "[NONAME] " + message

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
