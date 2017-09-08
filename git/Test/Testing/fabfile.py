from fabric.api import *
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import subprocess
import sys
import time
import signal


tree=ET.parse("variables.xml")
root = tree.getroot()
env.hosts=["localhost"]
timeStart=time.time()
logFile = "/tmp/TestLog"

@task
def testing(folderParameter='all',parameterTG='all', parameterTC='all', parameterTarget='all'):
	variablesList=[]
	logTime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	allOpenFile = open('%s' % logFile, 'a')
	allOpenFile.write("%s \n" % logTime)
	allOpenFile.close()
	for folder in root.findall('folder'):
		nameFolder = folder.get('name')
		if nameFolder == folderParameter or folderParameter == 'all':
			for TG in folder.findall('TG'):
				nameTG = TG.get('name')
				if nameTG == parameterTG or parameterTG == 'all':
					for TC in TG.findall('TC'):
						nameTC = TC.get('name')
						openFile = open('%s.%s.%s' % (logFile,nameFolder,nameTC), 'a')
						openFile.write("%s \n" % logTime)
						openFile.close()
						if nameTC == parameterTC or parameterTC == 'all':
							for TARGET in TC.findall('TARGET'):
								targetIP=TARGET.get('ip')
								if targetIP == parameterTarget or parameterTarget == 'all':
									for variables in TARGET.findall('variables'):
										variablesList.append(variables.text)
									xmlVariable = ' '.join(str(i) for i in variablesList)
									try:
										pid=os.fork()
										if pid == 0:
											commandParameterConstruct = 'ssh %s %s' % (targetIP, xmlVariable)
											shellCommand = [commandParameterConstruct]
											process = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
											while(process.poll() == None):
												timeNow=time.time()
												processEndTime = int(timeNow - timeStart)
												sys.stdout.flush()
												openFile = open('%s.%s.%s' %(logFile, nameFolder,nameTC), 'a')
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
										print("Error at running TC")
										allOpenFile = open('%s' % logFile, 'a')
										allOpenFile.write("Error at running TC")
										
									lista=[]

