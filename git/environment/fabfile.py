from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile = "/home/marius/script/fab/git/environment/logFile.txt"
path="/media/marius"

#Create folder timestamp with 4 subfolders
#@task
#@parallel
def fileCreation(projectName):
	if os.path.exists("%s/%s" % (path,projectName)):
		print "This project already exists"
		raise SystemExit()
	build = os.path.join("%s/%s/build" % (path,projectName))
	sdk = os.path.join("%s/%s/sdk" % (path,projectName))
	source = os.path.join("%s/%s/source" % (path,projectName))
	binary = os.path.join("%s/%s/binary" % (path,projectName))
	sourceTimeStamp = os.path.join("%s/" % source, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	binaryTimeStamp = os.path.join("%s/" % binary, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	try:
		os.makedirs(build)
		os.makedirs(sdk)
		os.makedirs(source)
		os.makedirs(binary)
		os.makedirs(sourceTimeStamp)
		os.makedirs(binaryTimeStamp)
		sudo("echo -e '%s \n%s \n%s \n%s\n%s \n%s \n' >> %s" % (build, sdk, source, binary, sourceTimeStamp, binaryTimeStamp, logFile))
		return (build, sdk, source, binary, sourceTimeStamp, binaryTimeStamp)
	except:
		print "Error at creating timestamps"
		#raise SystemExit()
