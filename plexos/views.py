# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate 
from .models import *
import subprocess
import os
import re
import os.path

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Create your views here.

from django.http import HttpResponse


from django.contrib.auth import (login as auth_login,  authenticate)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def login(request):
	_message = ""
	if request.method == 'POST':
		_username = request.POST['username']
		_password = request.POST['password']
		user = authenticate(username=_username, password=_password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(reverse('connect'))
			else:
				_message = 'Your account is not activated'
		else:
			_message = 'Invalid login, please try again.'
	t = loader.get_template("login.html")
	c = dict({"message": _message})
	return HttpResponse(t.render(c, request=request)) 


		
@login_required
def profile(request):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	if request.method == "GET": 
		return render(request, "profile.html")

	

@login_required
def connect(request): 
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	if request.method == "GET": 
		return profile(request)
	elif request.method == "POST":
		if request.POST.get('connectButton'): 
			username = request.POST['username']
			password = request.POST['password']
			server = request.POST['server']
			message = ""
			userInfo = ""
			folder = dict()
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/connect.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')
			stdout,stderr = p.communicate()
			folder["db1"] = {"1.1", "0.1"}
			folder["db2"] = {"1.3", "0.1"}
			#Taking tooo lone
			#for line in stdout.splitlines(): 
			#	if username in line: 
			#		datasetList = re.findall(r'dataset (.*?) version', line, re.DOTALL)
			#		dataset = ""
			#		for words in datasetList: 
			#			dataset += str(words)
			#		versionList = re.findall(r'version (.*?)$', line, re.DOTALL)
			#		version = ""
			#		for words in versionList: 
			#			version += str(words) 
			#		if dataset in folder: 
			#			folder[dataset].append(version)
			#		else: 
			#			folder[dataset]= [version]
			if p.returncode != 0: 
				#raise RuntimeError("%r failed, status code %s stdout %r stderr %r" % (
				#	['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/connect.py')], p.returncode, stdout, stderr))
				message = dict({"value" : 'Error Connecting to server. Ensure that you entered the corrent server, username and password. Please try again', "type" : "error"})
			else:
				userLen = UserInfo.objects.filter(Username=username)
				if userLen == 0: 
					userInfo = UserInfo.create(server, username, password)
				else: 
					userInfo = UserInfo.objects.filter(Username=username)[0]
				message = dict({"value" : 'Successfully Connected to Server', 
							"type" : "success"}) 
			t = loader.get_template("profile.html")
			c = dict({"message": message, "userInfo" : userInfo, "folder": folder})
			return HttpResponse(t.render(c, request=request)) 