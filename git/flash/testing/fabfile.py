from fabric.api import *
from datetime import datetime
import os
import subprocess
import sys
import time
import signal

logFile = "/tmp/flashLog"
autoEnvPath = './AutoEnv.sh'
flashDictionary = {'A' : ['A1','A2','A3'], 'B' : ['B1','B2','B3','B4']}
timeStart=time.time()




@task
def flash(array):
	logTime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	allOpenFile = open('%s' % logFile, 'a')
	allOpenFile.write("%s \n" % logTime)
	allOpenFile.close()
	keyCheck = False
	for key, values in flashDictionary.iteritems():
		if array == key or array == 'all':
			keyCheck = True
			for value in values:
				try:
					pid = os.fork()
					if pid == 0:
						autoEnvPathParameter = '%s %s %s' % (autoEnvPath, value, value)
						shellCommand = [autoEnvPathParameter]
						process = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
						openFile = open('%s%s.%s' % (logFile, key, value), 'a')
						openFile.write("%s \n" % logTime)
						openFile.close()
						while(process.poll() == None):
							timeNow=time.time()
							processEndTime = int(timeNow - timeStart)
							sys.stdout.flush()
							openFile = open('%s%s.%s' %(logFile, key,value), 'a')
							allOpenFile = open('%s' % logFile, 'a')
							for line in iter(process.stdout.readline, b''):
								print(line.rstrip())
								openFile.write(line)
								allOpenFile.write(line)
								break
							if processEndTime >= 3600:
								os.killpg(os.getpgid(process.pid), signal.SIGTERM)
						return
				except:
					print("Error at flashing %s" % value)
					allOpenFile = open('%s' % logFile, 'a')
					allOpenFile.write("Error at flashing %s \n" % value)
	if array != key and keyCheck == False:
		print("Error no such key")
