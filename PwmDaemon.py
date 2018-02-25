#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
import time
from daemon import runner

params = sys.argv

class PwmDaemon():
    def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/dev/null'
		self.pidfile_path =  '/tmp/foo.pid'
		self.pidfile_timeout = 5
		self.mode = int(params[2])
		self.ch = int(params[3])
		self.freq = int(params[4])
		self.dc = int(params[5])
		if(self.mode == 10):
			GPIO.setmode(GPIO.BOARD)
		else:
			GPIO.setmode(GPIO.BCM)
		
    def run(self):
		GPIO.setup(self.ch, GPIO.OUT)
		p = GPIO.PWM(self.ch, self.freq)
		p.ChangeDutyCycle(self.dc)
		p.start(self.dc)
		try:
			while(True):
				print "running"
				pass
		except KeyboardInterrupt:
			p.stop()
		
pwmDaemon = PwmDaemon()
daemon_runner = runner.DaemonRunner(pwmDaemon)
daemon_runner.do_action()
