#!/usr/bin/env python

#simple program to move syringe pump a set distance when a button is pushed.
import sys
import os
import pygame
from pygame import locals
import time
import RPi.GPIO as gpio
import spidev

#set up gpio correctly
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

#set gpio pin numbers 
DIR_0 = 11
STEP_0 = 13
SLEEP = 15

#Standard increment for movement
STD_INC = 600

#wait time
WAIT = 0.998

gpio.setup(SLEEP, gpio.OUT, initial = gpio.HIGH)
gpio.setup(STEP_0, gpio.OUT, initial = gpio.HIGH)
gpio.setup(DIR_0, gpio.OUT, initial = gpio.HIGH)

#initialize pygame stuff
#os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.flip()

pygame.joystick.init() #pygame joystick device system (for usb gamepad)

deadZone = 0.6 # make a wide deadzone
m1 = 0 # motor 1 (1 = forward / 2 = backwards)
m2 = 0 # motor 2 (1 = forward / 2 = backwards)
try:
   j = pygame.joystick.Joystick(0) # create a joystick instance
   j.init() # init instance
   print 'Enabled usb joystick: ' + j.get_name()
except pygame.error:
   print 'no usb joystick found.'

#SPI Joystick setup
spi = spidev.SpiDev()
spi.open(0,0)

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

	def move(self, direction):
		gpio.output(SLEEP, gpio.HIGH)
		
		if direction > 0:
			gpio.output(self.dir,  gpio.HIGH) 
			#self.state = "push"
		elif direction < 0: 
			gpio.output(self.dir, gpio.LOW)
			#self.state = "pull"
		
		else: 
			return
	
		for x in range(self.steps):
			gpio.output(self.step, gpio.HIGH)
			time.sleep(0.002)

			gpio.output(self.step, gpio.LOW)
			time.sleep(WAIT)

	#def sleep(self):
	#	gpio.output(SLEEP, gpio.LOW)

pump0 = Pump(STD_INC, DIR_0, STEP_0)
#pump1 = Pump(STD_INC, DIR_1, STEP_1)
#pump2 = Pump(STD_INC, DIR_2, STEP_2)
#pump3 = Pump(STD_INC, DIR_3, STEP_3)

#no movement at 0, pull if < 0, push if > 0
pump_m = [0,0,0,0]
#analog channels
CHANNEL_NUM = 4

#infiniloop for input
while(True):
	#cycle through the possible channels and set the movement integers based on the input from the channels
	for x in range(CHANNEL_NUM):
		joy_value = ReadChannel(x)
		
		print joy_value
		#joystick center is supposed to be 511.5
		if joy_value < 500:
#			pump_m[x] = -1 
			print 

		elif joy_value > 530:
			pump_m[x] = 1

		else:
			pump_m[x] = 0

	for e in pygame.event.get(): #iterate over pygame event stack
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_w: #forward motion on pump0
				print "W pressed"
				pump_m[0] = 1
		 	elif e.key == pygame.K_s: #backward motion on pump0
				print "S pressed"
				pump_m[0] = -1
			elif e.key == pygame.K_ESCAPE:
				sys.exit(1)

		elif e.type == pygame.KEYUP:
			if e.key == pygame.K_w or e.key == pygame.K_s:
				print "Key released" #Stop pump0
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
	#pump1.move(pump_m[1])
	#pump2.move(pump_m[2])
	#pump3.move(pump_m[3])			


gpio.cleanup()
