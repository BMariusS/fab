#IMPORTS
from fabric.api import *
from fabric.network import disconnect_all
from pyunpack import Archive
from environment import fabfile
import os.path
import zipfile
import fnmatch

 
#VARIABILES
path = '/home/marius/fab/'
env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile="/home/marius/script/fab/git/logFile.txt"
mailFile="/home/marius/script/fab/git/mails.txt"
script = "/home/marius"
pathMedia = "/media/marius"

#FUNCTIONS
def checkMailCommand():
	mailCommand = run ("type -P mail &>/dev/null && echo '"'Found'"' || echo '"'Not Found'"'")
	if mailCommand == "Not Found":
		print "Command mail does not exist"
		raise SystemExit()

#Check python module
def checkPyunpack():
	pyunpackModule = run("python -c '"'import pyunpack'"' && echo '"'Found'"' || echo '"'Not Found'"'")
	return pyunpackModule

def sendMailSuccess():
	checkMailCommand()
	if os.path.exists("%s" % mailFile):
		mails = sudo("cat %s | tr '\n' ',' " % mailFile)
		sudo("echo 'All steps from the script were executed with success' | mail -s 'Success' %s" % mails)
	else:
		print "Mail file doesn't exist"



def sendMailError():
	checkMailCommand()
	if os.path.exists("%s" % mailFile):
		mails = sudo("cat %s | tr '\n' ',' " % mailFile)
		try:
			if os.path.exists("%s" % logFile):
				sudo("echo 'There was an error with the program' | mail -s 'Error' %s -A %s" % (mails,logFile))
			else:
				print "Error attaching file"
		except:
			print "Error sending mail"
	else:
		print "Mail file doesn't exist"



def connection():
	try:
		run("hostname")
	except:
		abort("Connection failed")


#Clone for Method 0
@task
def gitClone(folder):
	if os.path.exists("%s%s/" % (path,folder)):
		sudo("echo 'Clone already exists' > %s" % logFile)
		with cd("%s" % path):
			sudo("rm -rf %s | echo 'Clone has been deleted' > %s" % (folder,logFile))
	with settings(warn_only=True):
		with cd("%s" % path):
			clone = sudo("git clone https://github.com/BMariusS/fab.git")
			if clone.return_code == 0:
				sudo("echo '%s' > %s" % (clone,logFile))
			else:
				sudo("echo '%s' > %s" % (clone,logFile))
				sendMailError()
				print "Error at cloning"
				raise SystemExit()


#Checkout for Method 0
@task
def gitCheckout(branch):
	with settings(warn_only=True):
		with cd("%s/fab/git" % path):
			checkout = sudo("git checkout %s" % branch)
			if checkout.return_code == 0:
				sudo("echo '%s' >> %s" % (checkout,logFile))
			else:
				sudo("echo '%s' >> %s" % (checkout,logFile))
				sendMailError()
				print "Error at checkout"
				raise SystemExit()

 
#Function to find Method 0 path and refresh the path
def find(name, path):
	for root, dirs, files in os.walk(path):
		if name in files:
			return os.path.join(root)


@task
def scriptCall():
	with settings(warn_only=True):
		scriptCall = sudo("%s/Practica/shellScript.sh" % script)
		if scriptCall.return_code == 0:
			sudo("echo '%s' >> %s" % (scriptCall,logFile))
			sendMailSuccess()
		else:
			sudo("echo '%s' >> %s" % (scriptCall,logFile))
			sendMailError()
			print "Error at calling the script"
			raise SystemExit()


#Display logFile
def displayLog():
	try:
		sudo("cat %s" % logFile)
	except:
		sendMailError()
		abort("Error at displaying logFile")


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
def timeStampsFolders(projectName,branch):
	try:
		timeStampPath = fabfile.timeStamps(projectName)
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
					else:
						sudo("echo '%s' >> %s" % (checkout,logFile))
						sendMailError()
						print "Error at checkout"
						raise SystemExit()
			else:
				sudo("echo '%s' >> %s" % (cloneSource,logFile))
				sendMailError()
				print "Error at cloning"
				raise SystemExit()



@task	
def moveSDK(projectName):
	if os.path.exists("%s/%s/sdk/" % (pathMedia,projectName)) and not os.listdir("%s/%s/sdk/" % (pathMedia,projectName)) == []:
		for fileArchive in os.listdir("%s/%s/sdk/" % (pathMedia,projectName)):
				if fileArchive.endswith(".zip"):
					if not fileArchive in os.listdir("%s/%s/build/" % (pathMedia,projectName)):
						put("%s/%s/sdk/%s" % (pathMedia,projectName,fileArchive), "%s/%s/build" % (pathMedia,projectName), use_sudo=True)
					else:
						print "The folder %s already exists on server" % fileArchive
				else:
					print "This %s/%s/sdk/%s is not an archive" % (pathMedia,projectName,fileArchive)
	else:
		print "There is nothing in %s/%s/sdk/" % (pathMedia,projectName)


@task
def unzip(projectName):
	unzip=checkPyunpack()
	if unzip == "Found":
		for serverArchive in os.listdir("%s/%s/build/" % (pathMedia,projectName)):
			if serverArchive.endswith(".zip"):
				checkContent = zipfile.ZipFile('%s' % serverArchive, 'r').namelist()
				for files in checkContent:
					if not files in os.listdir("%s/%s/build/" % (pathMedia,projectName)):
						Archive('%s' % serverArchive).extractall('%s/%s/build/' % (pathMedia,projectName)) #unzips test.zip from current directory to sdk path 
					else:
						print "The content of the %s archive is already extracted or has files with the same name" % serverArchive
						raise SystemExit()
	else:
		print "Error no pyunpack module installed"
		raise SystemExit()


#@task
#@parallel
#def final(cloneParameter='fab',checkoutParameter='master'):
	#connection()
	#gitClone(cloneParameter)
	#gitCheckout(checkoutParameter)
	#scriptCall()
	#disconnect_all()
	#clonePath = find('fabfile.py', '/home/marius/fab/%s' % cloneParameter)
	#os.chdir("%s" % clonePath) #refresh the directory after removing the clone
	#os.system("/bin/bash") #stay in the directory after executing the script
