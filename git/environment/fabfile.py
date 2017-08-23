from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile = "/home/marius/script/fab/git/environment/logFile.txt"

#Create folder timestamp with 4 subfolders
@task
@parallel
def fileCreation():
	timeStamp = os.path.join("/media/marius/", datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	source = os.path.join("%s/source" % timeStamp)
	build = os.path.join("%s/build" % timeStamp)
	sdk = os.path.join("%s/sdk" % timeStamp)
	binary = os.path.join("%s/binary" % timeStamp)
	try:
		timeStampLog = os.makedirs(timeStamp)
		sourceLog = os.makedirs(source)
		buildLog = os.makedirs(build)
		sdkLog = os.makedirs(sdk)
		binary = os.makedirs(binary)
		sudo("echo -e '%s \n%s \n%s \n%s\n%s \n' >> %s" % (timeStamp, source, build, sdk, binary, logFile))
		return (timeStamp, source, build, sdk, binary)
	except:
		print "Error at creating timestamps"
		#raise SystemExit()
