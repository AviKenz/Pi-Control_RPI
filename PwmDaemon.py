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
		self.ch = int(params[2])
		self.freq = int(params[3])
		self.dc = int(params[4])
    def run(self):
        #while True:
            #handlePwmOutput(self.ch, self.freq, self.dc)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.ch, GPIO.OUT)
		p = GPIO.PWM(self.ch, self.freq)
		p.ChangeDutyCycle(self.dc)
		p.start(self.dc)
		#log("t", "Look for a nicer Solution for the PWM")
		#log("d", "outputing PWM... Press CRTL + C to Stop")
		try:
			while(True):
				pass
		except KeyboardInterrupt:
			p.stop()
		
pwmDaemon = PwmDaemon()
daemon_runner = runner.DaemonRunner(pwmDaemon)
daemon_runner.do_action()
