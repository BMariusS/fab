#IMPORTS
from fabric.api import *
from fabric.network import disconnect_all
import os.path
from environment import fabfile

 
#VARIABILES
path = '/home/marius/fab/'
env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile="/home/marius/fab/fab/git/logFile.txt"
mailFile="/home/marius/fab/fab/git/mails.txt"
script = "/home/marius"


#FUNCTIONS
def checkMailCommand():
	mailCommand = run ("type -P mail &>/dev/null && echo '"'Found'"' || echo '"'Not Found'"'")
	if mailCommand == "Not Found":
		print "Command mail does not exist"
		raise SystemExit()

 	
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
 

def _find(name, path):
	for root, dirs, files in os.walk(path):
		if name in files:
			return os.path.join(root)


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

def displayLog():
	try:
		sudo("cat %s" % logFile)
	except:
		sendMailError()
		abort("Error at displaying logFile")


def prepareEnvironment():
	try:
		environment = fabfile.fileCreation()
		return environment
	except:
		print "Error at creating environment"
		#raise SystemExit()

def clone():
	#environment = prepareEnvironment()
	with settings(warn_only=True):
		with cd("%s" % environment[3]):
			cloneSource = sudo("git clone https://github.com/BMariusS/fab.git")
			if cloneSource.return_code == 0:
				sudo("echo '%s' >> %s" % (clone,logFile))
			else:
				sudo("echo '%s' >> %s" % (clone,logFile))
				#sendMailError()
				print "Error at cloning"
				raise SystemExit()
			

#@parallel
#def final(cloneParameter='fab',checkoutParameter='master'):
	#connection()
	#gitClone(cloneParameter)
	#gitCheckout(checkoutParameter)
	#scriptCall()
	#displayLog()
	#disconnect_all()
	#clonePath = _find('fabfile.py', '/home/marius/fab/%s' % cloneParameter)
	#with cd("/home/marius/script/fab/git/environment"):
		#sudo("fab fiileCreation")
	#os.chdir("%s" % clonePath)
	#os.system("/bin/bash")
