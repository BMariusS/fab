from fabric.api import *
import xml.etree.ElementTree as ET

tree=ET.parse("variables.xml")
root = tree.getroot()
env.hosts=["localhost"]

def testing(folderParameter='all',parameterTG='all', parameterTC='all'):
	lista=[]
	for folder in root.findall('folder'):
		nameFolder = folder.get('name')
		if nameFolder == folderParameter or folderParameter == 'all':
			for TG in folder.findall('TG'):
				nameTG = TG.get('name')
				if nameTG == parameterTG or parameterTG == 'all':
					for TC in TG.findall('TC'):
						nameTC = TC.get('name')
						if nameTC == parameterTC or parameterTC == 'all':
							for TARGET in TC.findall('TARGET'):
								for variables in TARGET.findall('variables'):
									lista.append(variables.text)
								variabile = ' '.join(str(i) for i in lista)
								print "%s %s" % (TARGET.get('id'),variabile)
								#sudo("echo '%s %s'" % (TARGET.get('id'),variabile))
								lista=[]

