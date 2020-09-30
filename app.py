from flask import Flask, render_template, Response, request, session, jsonify
import time
import threading
import random


# flask https://flask.palletsprojects.com/en/1.1.x/quickstart/
# invocation: python3.8 app.py

app = Flask(__name__)
app.secret_key = 'the random string'
app.debug = True
exporting_threads = {}
exporting_threads_outputs = {}
exporting_threads_stages = {}


class ExportingThread(threading.Thread):
	def __init__(self, threadID, email):
		self.threadID = threadID
		self.email = email
		self.progress = 0
		super().__init__()

	def run(self):
		global exporting_threads_outputs
		global exporting_threads_stages

		# main workflow goes there. update progress between steps

		# do something, step 1
		'''
		'''
		# update progress
		self.progress += 10
		exporting_threads_stages[threading.current_thread().threadID] = self.progress

		# do something, step 2
		'''
		'''
		# update progress
		self.progress += 10
		exporting_threads_stages[threading.current_thread().threadID] = self.progress

		# progress should reach 100 eventually
		for _ in range(8):
			time.sleep(2)
			self.progress += 10
			exporting_threads_stages[threading.current_thread().threadID] = self.progress
		#app.logger.info('thread %s finished', str(threading.get_ident()))
		app.logger.info('thread %s finished', str(threading.current_thread().threadID))
		exporting_threads_outputs[threading.current_thread().threadID] = 'Exporting workflow has finished for email ' + self.email



@app.route('/start', methods=['GET', 'POST'])
def start():
	global exporting_threads
	app.logger.info('start invoked')
	app.logger.info('email %s', request.form['email'])
	app.logger.info('password %s', request.form['password'])
	thread_id = random.randint(100,500)
	session['tid'] = thread_id
	exporting_threads[thread_id] = ExportingThread(threadID=thread_id, email=request.form['email'])
	exporting_threads[thread_id].start()
	app.logger.info('thread %s started', str(thread_id))
	data = {'message': 'Started', 'code': 'success'}
	resp = jsonify(success=True)
	resp.status_code = 200
	return resp;


@app.route('/result', methods=['GET', 'POST'])
def result():
	global exporting_threads_outputs
	app.logger.info('result invoked')
	result = exporting_threads_outputs[session['tid']]
	data = {'result': '<pre>'+result}
	resp = jsonify(data)
	return resp;

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Index')


@app.route('/progress')
def progress():
	app.logger.info('thread %s',  session['tid'] )
	if (session['tid'] in exporting_threads_stages):
		x = exporting_threads_stages[session['tid']]
	else:
		x = 0

	def generate():
		yield "data:" + str(x) + "\n\n"
		app.logger.info('stage %s ', str(x),  )

	return Response(generate(), mimetype= 'text/event-stream')

if __name__ == "__main__":
	app.run()