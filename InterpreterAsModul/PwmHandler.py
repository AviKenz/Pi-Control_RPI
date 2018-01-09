#!/usr/bin/python

def handlePwmOutput(pinNr, ch, freq, dc):
	log("d", "handlePwmOutput({}, {}, {})".format(ch, freq, dc))
	p = GPIO.PWM(ch, freq)
	p.start(dc)
	log("t", "Look for a nicer Solution for the PWM")
	log("d", "outputing PWM... Press CRTL + C to Stop")
	# testing subprocess
	subprocess.call(["ls -l"], shell=True)
	#try:
	#	while(True):
	#		pass
	#except KeyboardInterrupt:
	#	p.stop()
