import datetime
import time

def foo():
	print datetime.datetime.now()

iterations = 10

wait = 1

next_call = time.time()

while iterations > 0:
	foo()

	iterations -= 1
	next_call = next_call + wait

	time.sleep(next_call - time.time())