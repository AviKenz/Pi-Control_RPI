#!/usr/bin/python

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
p = GPIO.PWM(5, 1000)
p.start(1) 

