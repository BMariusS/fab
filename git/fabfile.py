#IMPORTS
from fabric.api import *
from fabric.network import disconnect_all
#from environment import fabfile
import os.path

 
#VARIABILES
path = '/home/marius/fab/'
env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
logFile="/home/marius/script/fab/git/logFile.txt"
mailFile="/home/marius/script/fab/git/mails.txt"
script = "/home/marius"

#FUNCTIONS
def checkMailCommand():
	mailCommand = run ("type -P mil &>/dev/null && echo '"'Found'"' || echo '"'Not Found'"'")
	if mailCommand == "Not Found":
		sudo("echo 'Command mail does not exist' >> %s" % logFile)
		raise SystemExit()


def sendMailSuccess():
	checkMailCommand()
	if os.path.exists("%s" % mailFile):
		mails = sudo("cat %s | tr '\n' ',' " % mailFile)
		sudo("echo 'All steps from the script were executed with success' | mail -s 'Success' %s" % mails)
	else:
		sudo("echo 'Sending mail success failed' >> %s" % logFile)



def sendMailError():
	checkMailCommand()
	if os.path.exists("%s" % mailFile):
		mails = sudo("cat %s | tr '\n' ',' " % mailFile)
		try:
			if os.path.exists("%s" % logFile):
				sudo("echo 'There was an error with the program' | mail -s 'Error' %s -A %s" % (mails,logFile))
			else:
				sudo("echo 'Error attaching file' >> %s" % logFile)
		except:
			sudo("echo 'Error sending mail' >> %s" % logFile)
	else:
		sudo("echo 'Mail file doesn't exist' >> %s" % logFile)



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


@task
@parallel
def final(cloneParameter,checkoutParameter='master'):
	connection()
	gitClone(cloneParameter)
	gitCheckout(checkoutParameter)
	scriptCall()
	disconnect_all()
	clonePath = find('fabfile.py', '/home/marius/fab/%s' % cloneParameter)
	os.chdir("%s" % clonePath) #refresh the directory after removing the clone
	os.system("/bin/bash") #stay in the directory after executing the script
