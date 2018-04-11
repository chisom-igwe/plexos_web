#!/usr/bin/ python2

import subprocess
import xml.dom.minidom
from django.core.exceptions import ValidationError
from threading import Timer
from xml.dom.minidom import parse
'''
	This is where functions taht will be used by all the views will be stored
	such functions include a timeout function
'''

def file_size(value): # add this to some file where you can import it from
		limit = 20 * 1024 * 1024
		if value.size > limit:
			raise ValidationError('File too large. Size should not exceed 20 MB.')

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
	if int(object_dict.get('FuelEmiGen')) > 20 or int(object_dict.get('Nodes')) > 5: 
		message += "Please adjust these features and reupload the file"

	objects = collection.getElementsByTagName("t_attribute_data")

	duration_number = 0
	duration_value = ''

	for object in objects:
		object_id = object.getElementsByTagName('object_id')[0]
		attribute_id = object.getElementsByTagName('attribute_id')[0]
		value = object.getElementsByTagName('value')[0]

		if object_id.childNodes[0].data == '2' and attribute_id.childNodes[0].data == '43':
		   duration_number = int(value.childNodes[0].data); 

		if object_id.childNodes[0].data == '2' and attribute_id.childNodes[0].data == '42':
		   duration_value = int(value.childNodes[0].data); 

	print duration_number 
	print duration_value
	if duration_number <= 7 and duration_value == 1 or duration_number == 1 and duration_value == 2: 
		pass
	else: 
		message += "Please adjust your duration horizon and reupload your file. It can only be a maximum of 7 days (1 week)"

	return message
	
