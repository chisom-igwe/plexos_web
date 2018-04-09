import xml.etree.cElementTree as ET
import subprocess
from threading import Timer

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
