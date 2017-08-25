from fabric.api import *
from fabric.network import disconnect_all
from datetime import datetime
import os
from functools import wraps

env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile = "/home/marius/script/fab/git/environment/logFile.txt"
pathMedia="/media/marius"
import tarfile
	
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
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating source folder"
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
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating binary folder"
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
					print "Error at creating source and binary time stamp"
		except:
			print "Error at creating source and binary folders"
	if os.path.exists("%s/%s/source" % (pathMedia,projectName)) and os.path.exists("%s/%s/binary" % (pathMedia,projectName)):
		try:
			sourceTimeStamp = os.path.join("%s/%s/source" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			binaryTimeStamp = os.path.join("%s/%s/binary" % (pathMedia,projectName), datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
			os.makedirs(sourceTimeStamp)
			os.makedirs(binaryTimeStamp)
			sudo("echo -e '%s \n%s \n' >> %s" % (sourceTimeStamp, binaryTimeStamp, logFile))
			return (sourceTimeStamp, binaryTimeStamp)
		except:
			print "Error at creating source and binary time stamp"
		

@task
def prepareEnvironment(projectName):
	if os.path.exists("%s/%s" % (pathMedia,projectName)):
		print "This project already exists"
		raise SystemExit()
	try:
		build = os.path.join("%s/%s/build" % (pathMedia,projectName))
		sdk = os.path.join("%s/%s/sdk" % (pathMedia,projectName))
		os.makedirs(build)
		os.makedirs(sdk)
		sudo("echo -e '%s \n%s \n' >> %s" % (build, sdk, logFile))
	except:
		print "Error at creating build and sdk folders"



#Clone to the source time stamp folder
@task
def timeStampFolders(projectName,branch):
	try:
		timeStampPath = timeStamps(projectName)
	except:
		print "error at creating environment"
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
							if os.path.exists("%s/server/source/" % pathMedia):
								print "Source exiists"
							else:
								os.makedirs("%s/server/source/" % pathMedia)
							put('%s' % timeStampPath[0], '%s/server/source/' % pathMedia, use_sudo = True)
							print "Succes at moving projects on server"
						except:
							print "Error at moving projects on server"
							
					else:
						sudo("echo '%s' >> %s" % (checkout,logFile))
						#sendMailError()
						print "Error at checkout"
						raise SystemExit()
			else:
				sudo("echo '%s' >> %s" % (cloneSource,logFile))
				#sendMailError()
				print "Error at cloning"
				raise SystemExit()



@task	
def moveSDK(projectName):
	for sdkArchive in os.listdir("%s/%s/sdk/" % (pathMedia, projectName)):
		if sdkArchive.endswith(".tar.gz"):
			try:
				put('%s/%s/sdk/%s' % (pathMedia,projectName,sdkArchive), '%s/server/sdk/' % pathMedia, use_sudo = True)
			except:
				print "Error at moving on server"
		else:
			print "Not a tar archive"
			raise SystemExit()


@task
def unzip():
	#unzip=checkPyunpack()
	#if unzip == "Found":
	for serverArchive in os.listdir("%s/server/sdk/" % pathMedia):
		if serverArchive.endswith(".tar.gz"):
			try:
				tarfile.open('%s/server/sdk/%s' % (pathMedia,serverArchive)).extractall('%s/server/sdk/' % pathMedia)
				#Archive('%s' % serverArchive).extractall('%s/server/sdk/' % pathMedia) #unzips test.tar.gz from current directory to sdk path
			except:
				print "Error at unziping"
		else:
			print "Error no archive"
			raise SystemExit()
	#else:
		#print "Error no pyunpack module installed"
		#raise SystemExit()

@task
def runCMake(projectName):
	for cmakeFind in os.listdir("%s/server/sdk/example_project" % pathMedia):
		with settings(warn_only=True):
			with cd("%s/server/sdk/example_project/" % pathMedia):
				if cmakeFind == "CMakeLists.txt":
					cmake = sudo("cmake -H. -Bbuild")
					sudo ("cmake --build build -- -j3")
					if cmake.return_code == 0:
						print "CMake succes"
						make = sudo ("make %s/server/sdk/example_project/build/" % pathMedia)
						if make.return_code == 0:
							print "Make succes"
						else:
							print "Error at make"
					else:
						print "Error at calling CMakeLists.txt"


@task
def test(projectName,branch):
	timeStampFolders(projectName,branch)
	moveSDK(projectName)
	unzip()
	runCMake(projectName)

