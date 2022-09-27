#!/usr/bin/env python3
import queue
import threading
import time
import http.client
# Modified from: http://www.ibm.com/developerworks/aix/library/au-threadingpython/
# and fixed with try-except around urllib call
# runs = 5
count = 1000
queue = queue.Queue() # queue is synchronized, so caters for multiple threads
class ThreadUrl(threading.Thread):
	def __init__(self, queue, task_id, minhistory, shots, option):
		threading.Thread.__init__(self)
		self.queue = queue
		self.task_id = task_id
		self.minhistory = minhistory
		self.shots = shots
		self.option = option
		self.data = None # need something more sophisticated if the thread can run many times
	def run(self):
		#while True: # uncomment this line if a thread should run as many times as it can
		count = self.queue.get()
		host = "cxsqhxhxyl.execute-api.us-east-1.amazonaws.com"
		try:
			c = http.client.HTTPSConnection(host)
			json= '{ "minhistory": ' + str(self.minhistory) + ', "shots": ' + str(self.shots) + ', "option": ' + str(self.option) + '}'
			c.request("POST", "/default/function_one", json)
			response = c.getresponse()
			self.data = response.read().decode('utf-8')
			#print( self.data, " from Thread", self.task_id )
		except IOError:
			print( 'Failed to open ' , host ) # Is the Lambda address correct?
		#signals to queue job is done
		self.queue.task_done()
# The class definition ends - the function below is outside
# the class body, so not initially indented
time_itr = []

def parallel_run(minhistory, shots, runs, option):
	threads=[]
	#spawn a pool of threads, and pass them queue instance
	for i in range(0, runs):
		start = time.time()
		t = ThreadUrl(queue, i, minhistory, shots, option)
		threads.append(t)
		t.setDaemon(True)
		t.start()
		end = time.time()
		time_itr.append(end-start)
#populate queue with data
	for x in range(0, runs):
		queue.put(count)
	#wait on the queue until everything has been processed
	queue.join()
	results = [t.data for t in threads]
	print(results)
	return results, time_itr

# Not indented
# start = time.time()
# print( "Elapsed Time:", time.time() - start)
