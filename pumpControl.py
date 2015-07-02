#!/usr/bin/env python

#simple program to move syringe pump a set distance when a button is pushed.
import sys
import os
import pygame
from pygame import locals
import time
import RPi.GPIO as gpio

#set up gpio correctly
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.cleanup()

#set gpio pin numbers 
DIR = 11
STEP = 13
SLEEP = 15

#STD_INC for movement
STD_INC = 1

gpio.setup(SLEEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(STEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(DIR, gpio.OUT, initial = gpio.HIGH)

#initialize pygame stuff
#os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.flip()

#joystick stuff for later
pygame.joystick.init() # main joystick device system

deadZone = 0.6 # make a wide deadzone
m1 = 0 # motor 1 (1 = forward / 2 = backwards)
m2 = 0 # motor 2 (1 = forward / 2 = backwards)
try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'Enabled joystick: ' + j.get_name()
except pygame.error:
   print 'no joystick found.'


#pump class for pump control methods
class Pump:
	def __init__(self, steps):
		self.steps = steps
		#self.state = "still"

	#def update(self):


	def move(self, direction):
		gpio.output(SLEEP, gpio.HIGH)
		
		if direction > 0:
			gpio.output(DIR,  gpio.HIGH) 
			#self.state = "push"
		elif direction < 0: 
			gpio.output(DIR, gpio.LOW)
			#self.state = "pull"
		
		else: 
			return
	
		for x in range(self.steps):
			gpio.output(STEP, gpio.HIGH)
			time.sleep(0.002)

			gpio.output(STEP, gpio.LOW)
			time.sleep(0.002)

	def sleep(self):
		gpio.output(SLEEP, gpio.LOW)

pump = Pump(STD_INC)

print "Press w to push, s to pull, press esc to quit."
sys.stdout.flush()

m1 = 0 #pump1
#infiniloop for input
while(True):
	#letter input (deprecated)
	#temp = raw_input()

	#if temp is "w":
	#	pump.move(1)

	#elif temp is "s":
	#	pump.move(-1)

	#elif temp is "q":
	#	print "exiting"
	#	sys.stdout.flush()

	for e in pygame.event.get(): #iterate over pygame event stack
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_w: #forward motion
				print "W pressed"
				m1 = 1
		 	elif e.key == pygame.K_s: #backward motion
				print "S pressed"
				m1 = -1
			elif e.key == pygame.K_ESCAPE:
				sys.exit(1)

		elif e.type == pygame.KEYUP:
			if e.key == pygame.K_w or e.key == pygame.K_s:
				print "Key released"
				m1 = 0

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

	pump.move(m1)

gpio.cleanup()
