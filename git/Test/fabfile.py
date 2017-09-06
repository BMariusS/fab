from fabric.api import *
from datetime import datetime

path = "/media/ssd/CVTESTS/BSP/"
logFile = "/tmp/TCLog"
logTime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

@task
def TC_1_1_1():
	try:
		openLog = open('%s' % logFile, 'a')
		tc_1_1_1 = run('%s/TG1.1/TC1.1.1/TC_1_1_1.sh' % path)
		openLog.write('%s \n' % logTime)
		openLog.write('%s' % tc_1_1_1)
	except:
		print "Error at TC_1_1_1"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TC_1_1_1')

@task
def TC_1_1_2():
	try:
		openLog = open('%s' % logFile, 'a')
		tc_1_1_2 = run('%s/TG1.1/TC1.1.1/TC_1_1_2.sh' % path)
		openLog.write('%s \n' % logTime)
		openLog.write('%s' % tc_1_1_2)
	except:
		print "Error at TC_1_1_2"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TC_1_1_2')

@task
def TC_1_2_1():
	try:
		openLog = open('%s' % logFile, 'a')
		tc_1_2_1 = run('%s/TG1.2/TC1.2.1/TC_1_2_1.sh' % path)
		openLog.write('%s \n' % logTime)
		openLog.write('%s' % tc_1_2_1)
	except:
		print "Error at TC_1_2_1"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TC_1_2_1')

@task
def TC_1_2_2():
	try:
		openLog = open('%s' % logFile, 'a')
		tc_1_2_2 = run('%s/TG1.2/TC1.2.1/TC_1_2_2.sh' % path)
		openLog.write('%s \n' % logTime)
		openLog.write('%s' % tc_1_2_2)
	except:
		print "Error at TC_1_2_2"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TC_1_2_2')

@task
def TG1_1():
	try:
		TC_1_1_1()
		TC_1_1_2()
	except:
		print "Error at TG1_1"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TG1_1')

@task
def TG1_2():
	try:
		TC_1_2_1()
		TC_1_2_2()
	except:
		print "Error at TG1_2"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at TG1_2')

@task
def all():
	try:
		TG1_1()
		TG1_2()
	except:
		print "Error at all"
		openLog = open('%s' % logFile, 'a')
		openLog.write('Error at all')
