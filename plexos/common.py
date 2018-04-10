import subprocess
import xml.dom.minidom

from threading import Timer
from xml.dom.minidom import parse
'''
	This is where functions taht will be used by all the views will be stored
	such functions include a timeout function
'''

def timeout(cmd):
	kill = lambda process: process.kill()
	my_timer = Timer(20.0, kill, [cmd])
	try:
		my_timer.start()
		stdout, stderr = cmd.communicate()
		return stdout, stderr, cmd.returncode
	finally:
		my_timer.cancel()

def parseXML(xmlfile):
	message = ''
	object_dict = ({'FuelEmiGen': 0, 'Nodes': 0})

	# Open XML document using minidom parser
	DOMTree = xml.dom.minidom.parse(xmlfile)
	collection = DOMTree.documentElement
	objects = collection.getElementsByTagName("t_object")

	for object in objects:
		class_id = object.getElementsByTagName('class_id')[0]
		if class_id.childNodes[0].data == '2' or class_id.childNodes[0].data == '5' or class_id.childNodes[0].data == '3': 
			object_dict['FuelEmiGen'] += 1
		elif class_id.childNodes[0].data == '33': 
			object_dict['Nodes'] += 1



	if int(object_dict.get('FuelEmiGen')) > 20 or int(object_dict.get('Nodes')) > 5: 
		message += "There is a problem with the following inputs: \n\n"
	if int(object_dict['FuelEmiGen']) > 20: 
		message += "The number of Fuel, Emissions and Generators exceeds 20"
	if int(object_dict['Nodes']) > 5: 
		message += "The number of Nodes exceeds 20"

	return message
	
