#!/usr/bin/env python

#simple program to move syringe pump a set distance when a button is pushed.
import sys
import os
import pygame
from pygame import locals
import time
import RPi.GPIO as gpio
import spidev
import threading

config = {}
execfile("pumpSettings.py", config)

print config

#set up gpio correctly
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

#set gpio pin numbers
DIR_PINS = config["direction_pins"]
STEP_PINS = config["step_pins"]
#DIR_0 = config["direction1"]
#STEP_0 = config["step1"]

#DIR_1 = config["direction2"]
#STEP_1 = config["step2"]

#DIR_2 = config["direction3"]
#STEP_2 = config["step3"]
#
#DIR_3= config["direction4"]
#STEP_3 = config["step4"]

#Standard increment for movement
STD_INC = config["steps"]

#wait time
WAIT = config["delay"]

#mode selection
MODE = config["mode"]

#number of pumps to control
NUM_PUMPS = config["pumps"]


#Function to read SPI data from MCP3008 chip
#channel must be int 0-7
def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data


#pump class for pump control methods
class Pump:
	def __init__(self, steps, dir_pin, step_pin):
		self.steps = steps
		self.dir = dir_pin
		self.step = step_pin

		gpio.setup(self.step, gpio.OUT, initial = gpio.HIGH)
		gpio.setup(self.dir, gpio.OUT, initial = gpio.HIGH)

	#move the pump one standard increment.
	def move(self, direction, num):
		gpio.output(SLEEP, gpio.HIGH)
		
		if direction > 0:
			gpio.output(self.dir,  gpio.HIGH) 
		elif direction < 0: 
			gpio.output(self.dir, gpio.LOW)
		
		else: 
			return
	
		try:
			print ("moving pump %", num)
			for x in range(self.steps):
				gpio.output(self.step, gpio.HIGH)
				time.sleep(0.002)

				gpio.output(self.step, gpio.LOW)
				time.sleep(WAIT)
		except (KeyboardInterrupt):
			print "Move stopped by KeyboardInterrupt"
			return


#set up pump objects and gpio controls.
pump_objs = []
for x in range(NUM_PUMPS):
	pump = Pump(STD_INC, DIR_PINS[x], STEP_PINS[x])
	pump_objs.append(pump)


#no movement at 0, pull if < 0, push if > 0
pump_m = [0,0,0,0]
#analog channels
CHANNEL_NUM = config["channels"]

#matrices for storage of movement variables for simultaneous movement.
pump_steps = [0,0,0,0]
pump_waits = [0,0,0,0]

def simultaneousMove(pump_waits, pump_steps, pump_m):
	#reset the wait time to a known value.
	WAIT = 0.002 

	#init my_threads storage, to keep track of timer threads outside loop.
	my_threads = [threading.Timer(), threading.Timer(), threading.Timer(), threading.Time()]
	
	#loop while there are steps to do
	while(x > 0 for x in pump_steps):
		#Timers, to handle waits simultaneously, correspond to pump numbers
		#Timer threads will sleep for the time given to them as the first arg
		#then execute the function given as their second arg based on the third
		#arg as the args for the called function.
		#The corresponding pump_steps entry is then decremented to reflect change
		if(pump_steps[0] > 0 and my_threads[0].is_alive() == False):
			my_threads[0] = threading.Timer(pump_waits[0], pump0.move, [pump_m[0], 0])
			my_threads[0].start()
			pump_steps[0] -= 1
		if(pump_steps[1] > 0 and my_threads[1].is_alive() == False):
			t1 = threading.Thread(pump_waits[1], pump1.move, [pump_m[1]], 1)
			t1.start()
			pump_steps[1] -= 1
		if(pump_steps[2] > 0 and my_threads[2].is_alive() == False):
			t2 = threading.Timer(pump_waits[2], pump2.move, [pump_m[2]], 2)
			t2.start()
			pump_steps[2] -= 1
		if(pump_steps[3] > 0 and my_threads[3].is_alive() == False):
			t3 = threading.Timer(pump_waits[3], pump2.move, [pump_m[3]], 3)
			t3.start()
			pump_steps[3] -= 1

#instant input instant 
if (mode == 0):
	#initialize pygame stuff
	#os.environ["SDL_VIDEODRIVER"] = "dummy"
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.flip()


	pygame.joystick.init() #pygame joystick device system (for usb gamepad)

	deadZone = 0.6 # make a wide deadzone

	try:
   		j = pygame.joystick.Joystick(0) # create a joystick instance
   		j.init() # init instance
   		print 'Enabled usb joystick: ' + j.get_name()
	except pygame.error:
   		print 'no usb joystick found.'


   	#SPI Joystick setup
	spi = spidev.SpiDev()
	spi.open(0,0)
	
	#infiniloop for input
	while(True):
		#cycle through the possible channels and set the movement integers based on the input from the channels
		for x in range(CHANNEL_NUM):
			joy_value = ReadChannel(x)
			
			print joy_value
			#joystick center is supposed to be 511.5
			if joy_value < 500:
				pump_m[x] = -1 
				print 

			elif joy_value > 530:
				pump_m[x] = 1

			else:
				pump_m[x] = 0

		for e in pygame.event.get(): #iterate over pygame event stack
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_w: #forward motion on pump0
					pump_m[0] = 1
			 	elif e.key == pygame.K_s: #backward motion on pump0
					pump_m[0] = -1
				elif e.key == spygame.K_d: #forward motion on pump1
					pump_m[1] = 1
				elif e.key == pygame.K_a: #backward motion on pump1
					pump_m[1] = -1
				elif e.key == pygame.K_UP:
					pump_m[2] = 1
				elif e.key == pygame.K_DOWN:
					pump_m[2] = -1
				elif e.key == pygame.K_RIGHT:
					pump_m[3] = 1
				elif e.key == pygame.K_LEFT:
					pump_m[3] = -1
				elif e.key == pygame.K_ESCAPE:
					gpio.cleanup()
					sys.exit(1)

			elif e.type == pygame.KEYUP:
				if e.key in (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
					#Stop pump0
					pump_m[0] = 0

			if e.type == pygame.locals.JOYAXISMOTION:	#read Analog stick motion
				x1, y1 = j.get_axis(0), j.get_axis(1) #Left Stick
				y2, x2 = j.get_axis(2), j.get_axis(3) #Right Stick (not in use)

				print x1
				print y1
				print x2
				print xy

				if x1 < -1 * deadZone:
					print "Left Joystick 1"

				if x1 > deadZone:
					print "Right Joystick 1"

				if y1 <= deadZone and y1 >= -1*deadZone:
					m1 = 0 #no motion

				if y1 < -1 *deadZone:
					print "Up Joystick 1"
					m1 = 1 #push forward

				if y1 > deadZone:
					print "Down Joystick 1"
					m1 = -1 #pull back
	
		
	
		#resolve movement
		pump0.move(pump_m[0])
		if num_pumps > 1: 
			pump1.move(pump_m[1])
		if num_pumps > 2:
			pump2.move(pump_m[2])
		if num_pumps > 3:
			pump3.move(pump_m[3])	

#single direction mode (keyboard entry)
elif(mode == 1):
	while(True):
		pump_num = raw_input("Pump to move: (type 'start' or 's' to move them and 'exit' or 'e' to exit)")
		if pump_num == "start" or pump_num == "s":
			simultaneousMove(pump_waits, pump_steps, pump_m)
		if pump_num == "exit" or pump_num == "e":
			gpio.cleanup()
			sys.exit(0)

		num_steps = raw_input("Number of steps to move it in: ")
		if (num_steps < 0):
			pump_m[pump_num] = -1
			pump_steps[pump_num] = abs(num_steps)

		else:
			direction = 1

		time = raw_input("Time to do steps in (seconds): ")
		pump_waits[pump_num] = (time/num_steps) - 0.002

		if pump_num == 0:
			pump0.move(direction)
		else:
			print "Invalid pump"

#alternating direction mode (keyboard entry)
#elif(mode == 2):
	#while(True):
		#pum
	
	#gpio.cleanup()
