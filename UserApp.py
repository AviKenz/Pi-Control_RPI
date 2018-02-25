#!/usr/bin/python

import PiControlApi as API


# start of programm
if __name__ == "__main__":
	API.log("d", "__main__")
	#handleParam()
	if(API.getName() == API.SWITCH_CONTROL_NAME):
		API.handleSwitchControl()
	elif(API.getName() == API.BUTTON_CONTROL_NAME):
		API.handleButtonControl()
	elif(API.getName() == API.BLINK_CONTROL_NAME):
		API.handleBlinkControl()
	elif(API.getName() == API.PWM_CONTROL_NAME):
		API.handlePwmControl()
	else:
		API.log("t", "Control Handler not implemented yet...")
		
		
		
		
		
		
		
		
		
		
		
		
		
