#!/usr/bin/python

import sys

initialized = False
args = sys.argv
	
def init(pArgs):
	args = pArgs
	initialized = True
	print "INIT.... after {}".format(initialized)

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
