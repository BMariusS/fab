#IMPORT
from fabric.api import *
from fabric.network import disconnect_all
#from fabric.utils import abort
#from fabric.utils import puts
import os.path
import sys

#VARIABILE
cale = '/home/marius'
env.hosts=["localhost"]
env.user="marius"
env.password="rootTest"
#comanda="|& tee -a  /home/marius/git/test.txt"
logFile="/home/marius/git/test.txt"


#TESTE
def gitCloneTest():
	with settings(warn_only=True):
		with cd("%s/git" % cale):
			clona = sudo("git clone https://github.com/BMariusS/fab.git")
			if clona.return_code == 0:
				sudo("echo '%s' > /home/marius/git/test.txt" % clona)
			else:
				sudo("echo '%s' > /home/marius/git/test.txt" % clona)
				print "Eroare la clonare"
				raise SystemExit()
				#abort("eroare la clonare")


#FUNCTII
def conexiune():
	try:
		run("hostname")
	except:
		abort("Conexiune nereusita")



def gitClone():
	if os.path.exists("%s/git/fab" % cale):
		sudo("echo 'Clona deja exista' > %s" % logFile)
	else:	
		#with cd("%s/git" % cale):
			#sudo("git clone https://github.com/BMariusS/fab.git %s" % comanda)
		with settings(warn_only=True):
			with cd("%s/git" % cale):
				clona = sudo("git clone https://github.com/BMariusS/fab.git")
				if clona.return_code == 0:
					sudo("echo '%s' > %s" % (clona,logFile))
				else:
					sudo("echo '%s' > %s" % (clona,logFile))
					print "Eroare la clonare"
					raise SystemExit()


def gitPull():
	with settings(warn_only=True):
		with cd("%s/git/fab/git" % cale):
			#if run("git pull %s" % comanda).failed:
				#sudo("git pull %s" % comanda)
			pull = sudo("git pull")
			if pull.return_code == 0:
				sudo("echo '%s' >> %s" % (pull,logFile))
			else:
				sudo("echo '%s' >> %s" % (pull,logFile))
				print "Eroare la pull"
				raise SystemExit()
		


def gitCheckout():
	with settings(warn_only=True):
		with cd("%s/git/fab/git" % cale):
			checkout = sudo("git checkout fab2")
			if checkout.return_code == 0:
				sudo("echo '%s' >> %s" % (checkout,logFile))
				#sudo("tree %s" % comanda)
			else:
				sudo("echo '%s' >> %s" % (checkout,logFile))
				print "Eroare la checkout"
				raise SystemExit()


def apelare():
	with settings(warn_only=True):
		apelare = sudo("%s/Practica/shellScript.sh" % cale)
		if apelare.return_code == 0:
			sudo("echo '%s' >> %s" % (apelare,logFile))
		else:
			sudo("echo '%s' >> %s" % (apelare,logFile))
			print "Eroare la apelarea scriptului"
			raise SystemExit()

@parallel
def final():
	conexiune()
	gitClone()
	gitPull()
	gitCheckout()
	apelare()
	disconnect_all()
