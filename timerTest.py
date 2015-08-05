#Basic timer test
import threading
import datetime
import time

def foo():
	print datetime.datetime.now()

print datetime.datetime.now()

iterations = 10

wait = 1

thread = None

next_call = time.time()

while iterations > 0:
	if thread == None or thread.is_alive() == False:
		next_call = next_call + wait
		thread = threading.Timer(next_call - time.time(), foo)
		thread.start()
		iterations -= 1
