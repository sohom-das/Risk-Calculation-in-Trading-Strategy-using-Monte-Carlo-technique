import os
import logging
import statistics
import csv

from flask import Flask, request, render_template

from parallel_lambda import parallel_run




app = Flask(__name__)

# various Flask explanations available at:https://flask.palletsprojects.com/en/1.1.x/quickstart/

def doRender(tname, values={}):
	if not os.path.isfile( os.path.join(os.getcwd(),'templates/'+tname) ): #No such file
		return render_template('calculator.htm')
	return render_template(tname, **values)
	
@app.route('/hello')
# Keep a Hello World message to show that at least something is working

@app.route('/calculator', methods=["GET"])
def cal_render():
	return render_template('calculator.htm')

def hello():
	return 'Hello World!'
	

var95 = []
var99 = []

var95_means = []
var99_means = []


mHist_lst = []
shots_lst = []
runs_lst = []
option_lst = []
service_lst = []

# rowHeader = ['service_lst', 'mHist_lst', 'shots_lst', 'runs_lst', 'option_lst', 'var95_means', 'var99_means']
@app.route('/calculator', methods=['POST'])
def calculator():
	var95.clear()
	var99.clear()
	var95_means.clear()
	var99_means.clear()
	
	mHist_lst.clear()
	shots_lst.clear()
	runs_lst.clear()
	option_lst.clear()
	service_lst.clear()
	
	import http.client
	if request.method == 'POST':
		m = request.form.get('minhistory')
		s = request.form.get('shots')
		r = int(request.form.get('runs'))
		option = request.form.get('option')
		
		print(m, s, r, option)
		vals, times = parallel_run(m,s,r, option)
		
		print("/n*********************************/n")
		print(vals)
		print("/n**********************Time starts here *********************/n")
		print(times)
		print("/n**********************Time ends here *********************/n")
		for i in vals:
			l = eval(i)
			var95.append(l[0])
			var99.append(l[1])

			var95_means.append(statistics.mean(l[0]))
			var99_means.append(statistics.mean(l[1]))
			
			
		for z in range(r):
			mHist_lst.append(m)
			shots_lst.append(s)
			runs_lst.append(r)
			service_lst.append("Lambda")
			if option=='1':
				option_lst.append("Buy")
			else: option_lst.append("Sell")
			
			
		print("/n************************************/n")
		print(mHist_lst)
		print(shots_lst)
		print(runs_lst)
		print(option_lst)
		print(service_lst)
		print(var95_means, var99_means)
		
		#code for storing the data to a CSV file
		#specifying the file	
		#filename = r'/frontend/practice.csv'
		#checking the files exists or not
		#file_exists = os.path.isfile(filename)

		#f =  open(filename, 'a', newline="")
		#write = csv.writer(f)
		#if not file_exists:
			#write.writerow(rowHeader)
		#else:
			#write.writerows(zip(service_lst, mHist_lst, shots_lst, runs_lst, option_lst, var95_means, var99_means))

		#f.close()
		
			
		return doRender( 'calculator.htm',{'note': zip(service_lst, mHist_lst, shots_lst, runs_lst, option_lst, var95_means, var99_means, times)} )


var95_for_graph = []
var99_for_graph = []
var95_length = []
var99_length = []
var95_average_lst = []
var99_average_lst = []
@app.route('/charts', methods=['GET'])
def charts():
	var95_for_graph.clear()
	var99_for_graph.clear()
	var95_length.clear()
	var99_length.clear()
	var95_average_lst.clear()
	var99_average_lst.clear()
	for a in var95:
		for ele in a:
			var95_for_graph.append(ele)
	print("\n*************************************\n")
	print("This is var95_for_graph", var95_for_graph)
	print("length of var95_for_graph", len(var95_for_graph))
	
	
	for b in var99:
		for elements in b:
			var99_for_graph.append(elements)
			
	print("\n*************************************\n")
	print("This is var99_for_graph", var99_for_graph)
	print("length of var99_for_graph", len(var99_for_graph))
	
	var99_average = statistics.mean(var99_for_graph)
	
	for l in range(1, len(var95_for_graph)+1):
		var95_length.append(l)
		var95_average_lst.append(statistics.mean(var95_for_graph))
		
	for z in range(1, len(var99_for_graph)+1):
		var99_length.append(z)
		var99_average_lst.append(statistics.mean(var99_for_graph))
	
			
	return render_template('chart.htm', var95_lst = var95_for_graph, var99_lst = var99_for_graph, var95_ln = var95_length, var99_ln = var99_length, var95_avg = var95_average_lst, var99_avg = var99_average_lst)


 
# catch all other page requests - doRender checks if a page is available (shows it) or not (index)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def mainPage(path):
	return doRender(path)
@app.errorhandler(500)
# A small bit of error handling
def server_error(e):
 	logging.exception('ERROR!')
 	return """
 	An error occurred: <pre>{}</pre>
 	""".format(e), 500
if __name__ == '__main__':
 	# Entry point for running on the local machine
 	# On GAE, endpoints (e.g. /) would be called.
 	# Called as: gunicorn -b :$PORT index:app,
 	# host is localhost; port is 8080; this file is index (.py)
 	app.run(host='127.0.0.1', port=8080, debug=True)
