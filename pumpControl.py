#simple program to move syringe pump a set distance when a button is pushed.
import sys
import time
import RPi.GPIO as gpio

#set up gpio correctly
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

#set gpio pin numbers 
DIR = 11
STEP = 13
SLEEP = 15

#STD_INC for movement
STD_INC = 200

gpio.setup(SLEEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(STEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(DIR, gpio.OUT, initial = gpio.HIGH)

#pump class for pump control methods
class Pump:
	def __init__(self, steps):
		self.steps = steps

	def move(self, direction):
		gpio.output(SLEEP, gpio.HIGH)
		gpio.output(DIR,  gpio.HIGH if direction > 0 else gpio.LOW)

		for x in range(self.steps):
			gpio.output(STEP, gpio.HIGH)
			time.sleep(0.002)

			gpio.output(STEP, gpio.LOW)
			time.sleep(0.002)

pump = Pump(STD_INC)

print "Press w to push, s to pull, press q to quit."
sys.stdout.flush()

#infiniloop for input
while(True):
	temp = raw_input()

	if temp is "w":
		pump.move(1)

	elif temp is "s":
		pump.move(-1)

	elif temp is "q":
		print "exiting"
		sys.stdout.flush()

