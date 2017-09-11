from fabric.api import *
import glob
import os
from os.path import basename

env.hosts=["localhost"]


def RQMVariables(scriptName,*environmentVariables):
	for script in glob.glob("*.sh"):
		scriptWithoutExtension = os.path.splitext("%s" % script)[0]
		if scriptName == scriptWithoutExtension:
			callingScript = os.path.realpath(script)
			scriptVariables = ' '.join(str(i) for i in environmentVariables)
			sudo("%s %s" % (callingScript,scriptVariables))
