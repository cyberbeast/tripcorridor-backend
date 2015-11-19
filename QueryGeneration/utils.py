import settings
import time

class Logger:
	"A Class to log the outputs to file"
	def __init__(self,logfile = None, log = None):
		if logfile is None:
			self.logfile = settings.LOG_FILE
		else:
			assert isinstance(logfile,str)
			self.logfile = logfile

		if log is None:
			self.log = settings.LOG
		else:
			assert isinstance(log,bool)
			self.log = log

		self.handle = open(settings.LOG_DIR + '/' + self.logfile, 'w')

	def dump(self,data):
		if self.log:
			self.handle.write(str(data) + '\n')

	def close(self):
		self.handle.write("Logger exiting..." + '\n')
		self.handle.close()

class Timer:
	"A class to time the events and print elapse message"
	def __init__(self, message = "Time Elaspsed: "):
		self._message = message
		self.tic = None
		self.toc = None

	def start(self):
		self.tic = time.time()

	def stop(self):
		self.toc = time.time()

	def message(self):
		return self._message + str(self.toc - self.tic)

	def set_message(self, message):
		self._message = message

if __name__ == '__main__':
	log = Logger("logger_test.txt")
	log.dump("Hello this will be logged")
	log.close()
