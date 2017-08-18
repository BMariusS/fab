 #IMPORTS
 from fabric.api import *
 from fabric.network import disconnect_all
 import os.path
 
 #VARIABILES
 path = '/home/marius/fab'
 env.hosts=["localhost"]
 env.user="marius"
 env.password="rootTest"
 logFile="/home/marius/fab/git/logFile.txt"
 mailFile="/home/marius/fab/git/mails.txt"
 script = "/home/marius"
 
 
 '''#TESTS
 def gitCloneTest():
 	with settings(warn_only=True):
 		with cd("%s/git" % path):
 			clone = sudo("git clone https://github.com/BMariusS/fab.git")
 			if clone.return_code == 0:
 				sudo("echo '%s' > /home/marius/git/test.txt" % clone)
 			else:
 				sudo("echo '%s' > /home/marius/git/test.txt" % clone)
 				print "Error at clonning"
 				raise SystemExit()
 				#abort("eroare la clonare")
 
 
 def gitPull():
 	with settings(warn_only=True):
 		with cd("%s/git" % path):
 			#if run("git pull %s" % comanda).failed:
 				#sudo("git pull %s" % comanda)
 			pull = sudo("git pull")
 			if pull.return_code == 0:
 				sudo("echo '%s' >> %s" % (pull,logFile))
 			else:
 				sudo("echo '%s' >> %s" % (pull,logFile))
 				print "Error at pull"
 				raise SystemExit()
 '''
 
 
 
 
 #FUNCTIONS
-
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
 
 
 
 def gitClone():
 	if os.path.exists("%s/git/fab" % path):
 		sudo("echo 'Clone already exists' > %s" % logFile)
 		sudo("rm -rf %s/git/fab | echo 'Clone has been deleted' > %s" % (path,logFile))
 	#else:	
 		#with cd("%s/git" % cale):
 			#sudo("git clone https://github.com/BMariusS/fab.git %s" % comanda)
 	with settings(warn_only=True):
 		with cd("%s/git" % path):
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
 		with cd("%s/git" % path):
 			checkout = sudo("git checkout %s" % branch)
 			if checkout.return_code == 0:
 				sudo("echo '%s' >> %s" % (checkout,logFile))
 				#sudo("tree %s" % comanda)
 			else:
 				sudo("echo '%s' >> %s" % (checkout,logFile))
 				sendMailError()
 				print "Error at checkout"
 				raise SystemExit()
 
 
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
 		sudo("cat %s/git/logFile.txt" % path)
 	except:
 		sendMailError()
 		abort("Error at displaying logFile")
 
 @parallel
 def final(parameter):
 	connection()
 	gitClone()
 	gitCheckout(parameter)
 	scriptCall()
 	displayLog()
	disconnect_all()
