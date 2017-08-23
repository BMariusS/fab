from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile = "/home/marius/script/fab/git/environment/logFile.txt"
path="/media/marius/"

#Create folder timestamp with 4 subfolders
#@task
@parallel
def fileCreation(projectName):
	build = os.path.join("%s/build" % path)
	sdk = os.path.join("%s/sdk" % path)
	source = os.path.join("%s/source" % path)
	binary = os.path.join("%s/binary" % path)
	sourceTimeStamp = os.path.join("%s/" % source, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	binaryTimeStamp = os.path.join("%s/" % binary, datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	try:
		buildLog = os.makedirs(build)
		sdkLog = os.makedirs(sdk)
		sourceLog = os.makedirs(source)
		binary = os.makedirs(binary)
		sourceTimeStampLog = os.makedirs(sourceTimeStamp)
		binaryTimeStamp = os.makedirs(binaryTimeStamp)
		sudo("echo -e '%s \n%s \n%s \n%s\n%s \n%s \n' >> %s" % (build, sdk, source, binary, sourceTimeStamp, binaryTimeStamp, logFile))
		return (build, sdk, source, binary, sourceTimeStamp, binaryTimeStamp)
	except:
		print "Error at creating timestamps"
		#raise SystemExit()
