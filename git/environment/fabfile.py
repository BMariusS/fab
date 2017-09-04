from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os
import tarfile
import glob
import subprocess
import sys
import time
import signal
#import threading

#env.use_ssh_config = True
env.hosts=["localhost"]
#env.key_filename="~/.ssh/id_rsa"
#env.port = 22
logFile = "/home/marius/script/fab/git/environment/logFile"
pathMedia="/media/marius"
serverSDKPath = "%s/server/sdk" % pathMedia
serverSourcePath = "%s/server/source" % pathMedia
autoEnvPath = '/home/marius/script/fab/git/AutoEnv.sh'
flashDictionary = {'A' : ['A1','A2','A3'], 'B' : ['B1','B2','B3','B4']}
timeStart=time.time()

#rm -rf /media/marius/*/source/* /media/marius/server/sdk/* /media/marius/test/binary/* /media/marius/test/deploy/*
	
def timeStamps(projectName):
	if not os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
		try:
			source = os.path.join("%s/%s/source" % (pathMedia,projectName))
			os.makedirs(source)
			sudo("echo -e '%s \n' >> %s" % (source, logFile))
			if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					sudo("echo 'Error at creating source and binary time stamp' >> %s" % logFile)
		except:
			sudo("echo 'Error at creating source folder' >> %s" % logFile)
	if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and not os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
		try:
			binary = os.path.join("%s/%s/binary" % (pathMedia,projectName))
			os.makedirs(binary)
			sudo("echo -e '%s \n' >> %s" % (binary, logFile))
			if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					sudo("echo 'Error at creating source and binary time stamp' >> %s" % logFile)
		except:
			sudo("echo 'Error at creating binary folder' >> %s" % logFile)
	if not os.path.exists("%s/%s/source" % (pathMedia,projectName)) and not os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
		try:
			source = os.path.join("%s/%s/source" % (pathMedia,projectName))
			os.makedirs(source)
			binary = os.path.join("%s/%s/binary" % (pathMedia,projectName))
			os.makedirs(binary)
			sudo("echo -e '%s \n%s \n' >> %s" % (source, binary, projectName))
			if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
				try:
					sourceTimeStamp = os.path.join("%s/%s/source" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					binaryTimeStamp = os.path.join("%s/%s/binary" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
					os.makedirs(sourceTimeStamp)
					os.makedirs(binaryTimeStamp)
					sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
					return (sourceTimeStamp, binaryTimeStamp)
				except:
					sudo("echo 'Error at creating source and binary time stamp' >> %s" % logFile)
		except:
			sudo("echo 'Error at creating source and binary folders' >> %s" % logFile)
	if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
		try:
			sourceTimeStamp = os.path.join("%s/%s/source" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			binaryTimeStamp = os.path.join("%s/%s/binary" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			os.makedirs(sourceTimeStamp)
			os.makedirs(binaryTimeStamp)
			sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
			return (sourceTimeStamp, binaryTimeStamp)
		except:
			sudo("echo 'Error at creating source and binary time stamp' >> %s" % logFile)
		

@task
def prepareEnvironment(projectName):
	if os.path.exists("%s/%s" % (pathMedia,projectName)):
		sudo("echo 'This project already exists' >> %s" % logFile)
		raise SystemExit()
	try:
		build = os.path.join("%s/%s/build" % (pathMedia,projectName))
		sdk = os.path.join("%s/%s/sdk" % (pathMedia,projectName))
		os.makedirs(build)
		os.makedirs(sdk)
		sudo("echo -e '%s \n%s \n' >> %s" % (build, sdk, logFile))
	except:
		sudo("echo 'Error at creating build and sdk folders' >> %s" % logFile)


@task	
def moveSDK(projectName):
	for sdkArchive in os.listdir("%s/%s/sdk/" % (pathMedia, projectName)):
		if sdkArchive.endswith(".tar.gz"):
			try:
				put('%s/%s/sdk/%s' % (pathMedia,projectName,sdkArchive), '%s/' % serverSDKPath, use_sudo = True)
				sudo("echo 'SDK moved with success' >> %s" % logFile)
			except:
				sudo("echo 'Error at moving on server' >> %s" % logFile)
		else:
			sudo("echo 'Not a tar archive' >> %s" % logFile)
			raise SystemExit()


@task
def unzip():
	for serverArchive in glob.glob("%s/*.tar.gz" % serverSDKPath):
		if serverArchive.endswith(".tar.gz"):
			try:
				tarfile.open('%s' % serverArchive).extractall('%s/' % serverSDKPath)
				sudo("echo 'Archive unziped with success' >> %s" % logFile)
			except:
				sudo("echo 'Error at unziping' >> %s" % logFile)
		else:
			sudo("echo 'Error no archive' >> %s" % logFile)
			raise SystemExit()

@task
def runCMake():
	for cmakeFind in os.listdir("%s/example_project" % serverSDKPath):
		with settings(warn_only=True):
			with cd("%s/example_project/" % serverSDKPath):
				if cmakeFind == "CMakeLists.txt":
					cmake = sudo("cmake -H. -Bbuild")
					cmakeBuild = sudo ("cmake --build build -- -j3")
					if cmake.return_code == 0 and cmakeBuild.return_code == 0:
						sudo("echo 'CMake succes' >> %s" % logFile)
						make = sudo ("make %s/example_project/build/" % serverSDKPath)
						if make.return_code == 0:
							sudo("echo 'Make succes' >> %s" % logFile)
						else:
							sudo("echo 'Error at make' >> %s" % logFile)
					else:
						sudo("echo 'Error at calling CMakeLists.txt' >> %s" % logFile)


#Clone to the source time stamp folder
@task
def timeStampFolders(projectName,branch):
	global logFile
	try:
		timeStampPath = timeStamps(projectName)
	except:
		sudo("echo 'Error at creating environment' >> %s" % logFile)
	logFile="%s/logFile" % timeStampPath[0]
	with settings(warn_only=True):
		with cd("%s" % timeStampPath[0]):
			cloneSource = sudo("git clone https://github.com/BMariusS/fab.git")
			if cloneSource.return_code == 0:
				sudo("echo '%s' >> %s" % (cloneSource,logFile))
				with cd("%s/fab/git" % timeStampPath[0]):
					checkout = sudo("git checkout %s" % branch)
					if checkout.return_code == 0:
						sudo("echo '%s' >> %s" % (checkout,logFile))
						try:
							if os.path.exists("%s/" % serverSourcePath):
								sudo("echo 'Source exists' >> %s" % logFile)
							else:
								os.makedirs("%s/" % serverSourcePath)
							put('%s' % timeStampPath[0], '%s/' % serverSourcePath, use_sudo = True)
							sudo("echo 'Succes at moving projects on server' >> %s" % logFile)
							moveSDK(projectName)
							unzip()
							runCMake()
							if os.listdir("%s/example_project/build" % serverSDKPath) != []:
								folderTimeStamp = os.path.split(timeStampPath[0])
								try:
									get('%s/example_project/build' % serverSDKPath, '%s/%s/binary/%s' %(pathMedia,projectName,folderTimeStamp[-1]), use_sudo = True)
									sudo("echo 'Succes at getting the files from server' >> %s" % logFile)
								except:
									sudo("echo 'Error at getting the files from server' >> %s" % logFile)
						except:
							sudo("echo 'Error at moving projects on server' >> %s" % logFile)
							
					else:
						sudo("echo '%s' >> %s" % (checkout,logFile))
						print "Error at checkout"
						raise SystemExit()
			else:
				sudo("echo '%s' >> %s" % (cloneSource,logFile))
				print "Error at cloning"
				raise SystemExit()



@task
def getLastBuild(projectName):
	directoryTimeStamp=[]
	for directory in os.listdir("%s/%s/binary/" % (pathMedia,projectName)):
		directoryTimeStamp.append(directory)
	directoryTimeStamp.sort()
	try:
		put('%s/%s/binary/%s/build/' % (pathMedia,projectName,directoryTimeStamp[-1]), '%s/%s/deploy/' % (pathMedia,projectName), use_sudo = True)
		sudo("echo 'Success at moving binaries' >> %s" % logFile)
	except:
		sudo("echo 'Error at moving binaries' >> %s" % logFile)

@task
def scriptCall():
	with settings(warn_only=True):
		scriptCall = sudo("%s test" % autoEnvPath)
		if scriptCall.return_code == 0:
			sudo("echo '%s' >> %s" % (scriptCall,logFile))
		else:
			sudo("echo '%s' >> %s" % (scriptCall,logFile))
			print "Error at calling the script"
			raise SystemExit()

'''
exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name
      print_time(self.name, self.counter, 5)
      print "Exiting " + self.name

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1

@task
def testare():
	# Create new threads
	thread1 = myThread(1, "Thread-1", 1)
	thread2 = myThread(2, "Thread-2", 2)

	# Start new Threads
	thread1.start()
	thread2.start()


@task
def flashV2(array):
	for key, value in test.iteritems():
		if array == key:
			for i in value:
				try:
					print "test"
				except:
					print "Error"
'''

@task
#@parallel
def flash(array):
	for key, values in flashDictionary.iteritems():
		if array == key:
			for value in values:
				try:
					pid = os.fork()
					if pid == 0:
						autoEnvPathParameter = '%s %s %s' % (autoEnvPath, value, value)
						shellCommand = [autoEnvPathParameter]
						process = subprocess.Popen(shellCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
						while(process.poll() == None):
							timeNow=time.time()
							processEndTime = int(timeNow - timeStart)
							sys.stdout.flush()
							openFile = open('%s%s' %(logFile, value), 'a')
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
					allOpenFile = open('%s' % logFile, 'a')
					openFile.write("Error at flashing %s" % value)

@task
@parallel
def testing(projectName,branch,array):
	if os.path.exists("%s" % logFile):
		sudo("rm %s" % logFile)
	sudo("touch %s" % logFile)
	timeStampFolders(projectName,branch)
	getLastBuild(projectName)
	scriptCall()
	flash(array)
