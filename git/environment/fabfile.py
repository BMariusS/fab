rom fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"


def fileCreation():
	timeStamp = os.path.join("/media/marius/", datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
	build = os.path.join("%s/build" % timeStamp)
	sdk = os.path.join("%s/sdk" % timeStamp)
	source = os.path.join("%s/source" % timeStamp)
	try:
		timeStampLog = os.makedirs(timeStamp)
		buildLog = os.makedirs(build)
		sdkLog = os.makedirs(sdk)
		sourceLog = os.makedirs(source)
		sudo("echo -e '%s \n%s \n%s \n%s\n' >> /home/marius/script/fab/git/environment/logFile.txt" % (timeStamp, build, sdk, source))
	except:
		print "Error at creating timestamps"
raise SystemExit()
