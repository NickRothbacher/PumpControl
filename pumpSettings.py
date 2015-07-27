#Settings file for the pumpControl program, holds values for all the different variables involved in the program.

#GPIO pins used for the program, contains placeholders for the last three currently
direction_pins = [11, 16, 29, 32]
step_pins = [13, 18, 31, 36]

#standard number of steps per call of the move function
steps = 1

#standard delay for one call of the move function (seconds)
delay = 0.002 

#Operation mode for the program, 
# 0 for direct joystick or keyboard pumpControl
# 1 for single direction movement over a certain time
# 2 for alternating movement over a certain time
mode = 1

#number of pumps needed to be controlled by the program, 4 maximum currently
pumps = 4

#number of channels in use by the SPI interface
channels = 2

