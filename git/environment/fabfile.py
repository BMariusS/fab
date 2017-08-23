from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os
from functools import wraps

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile = "/home/marius/script/fab/git/environment/logFile.txt"
path="/media/marius"
	
@task
def timeStamps(projectName):
	if not os.path.exists("%s/%s/source" % (path,projectName)) and os.path.exists("%s/%s/binary" % (path,projectName)):
		try:
			source = os.path.join("%s/%s/source" % (path,projectName))
			os.makedirs(source)
			sudo("echo -e '%s \n' >> %s" % (source, logFile))
			if os.path.exists("%s/%s/source" % (path,projectName)) and os.path.exists("%s/%s/binary" % (path,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating source folder"
	if os.path.exists("%s/%s/source" % (path,projectName)) and not os.path.exists("%s/%s/binary" % (path,projectName)):
		try:
			binary = os.path.join("%s/%s/binary" % (path,projectName))
			os.makedirs(binary)
			sudo("echo -e '%s \n' >> %s" % (binary, logFile))
			if os.path.exists("%s/%s/source" % (path,projectName)) and os.path.exists("%s/%s/binary" % (path,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating binary folder"
	if not os.path.exists("%s/%s/source" % (path,projectName)) and not os.path.exists("%s/%s/binary" % (path,projectName)):
		try:
			source = os.path.join("%s/%s/source" % (path,projectName))
			os.makedirs(source)
			binary = os.path.join("%s/%s/binary" % (path,projectName))
			os.makedirs(binary)
			sudo("echo -e '%s \n%s \n' >> %s" % (source, binary, projectName))
			if os.path.exists("%s/%s/source" % (path,projectName)) and os.path.exists("%s/%s/binary" % (path,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (path,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating source and binary folders"

