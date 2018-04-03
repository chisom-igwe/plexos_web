# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from threading import Timer
from django.shortcuts import render, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages, auth
from django.contrib.auth import (authenticate, login as auth_login) 
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .common import *
from .models import *
from .forms import *
import subprocess
import re
import os
from os import path, listdir
from os.path import abspath, dirname, isfile, join

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Create your views here.

'''
	This is the view to login into the application 
	It asks for a users username and password 
	and redirects them to the profile page if logged in 
	or sends back to login page if there is an error
'''
def login(request):
	_message = ""
	if request.method == 'POST':
		_username = request.POST['username']
		_password = request.POST['password']
		user = authenticate(username=_username, password=_password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(reverse('profile'))
			else:
				_message = 'Your account is not activated'
		else:
			_message = 'Invalid login, please try again.'
	t = loader.get_template("login.html")
	c = dict({"message": _message})
	return HttpResponse(t.render(c, request=request)) 


		
@login_required
def profile(request):
	if request.method == "GET": 
		return render(request, "profile.html")
	elif request.method == "POST":
		if request.POST.get('connectButton'):
			#Get user defined values for username, password, server 
			username = request.POST['username']
			password = request.POST['password']
			server = request.POST['server']

			#initialize return message variable, userInfo variable and user folder 
			message = ""
			userInfo = ""
			folder = dict() 

			#make request to api 
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/connect.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')

			#get stdout,sterr based on timeout function
			stdout,stderr, returncode = timeout(p)

			#parse through stdout and get user datasets and versions. Also set message based on status of output 
			if returncode != 0: 
				message = dict({"value" : 'Error Connecting to server. Ensure that you entered the corrent server, username and password. Please try again', "type" : "error"})
			else:
				for line in stdout.splitlines(): 
					if username in line: 
						datasetList = re.findall(r'dataset (.*?) version', line, re.DOTALL)
						dataset = ""
						for words in datasetList: 
							dataset += str(words)
						versionList = re.findall(r'version (.*?)$', line, re.DOTALL)
						version = ""
						for words in versionList: 
							version += str(words) 
						if dataset in folder: 
							folder[dataset].append(version)
						else: 
							folder[dataset]= [version]

					userLen = len(UserInfo.objects.filter(Username=username))
					if userLen == 0: 
						userInfo = UserInfo.create(server, username, password)
					else: 
						userInfo = UserInfo.objects.filter(Username=username)[0]
					message = dict({'value' : 'Successfully Connected to Server', 'type' : 'success'}) 

			#set user sessions folder 
			request.session['folder'] = folder

			#set user sessions information 
			sessionInfo = dict({"username": username, "password": password, "server": server})
			request.session['sessionInfo'] = sessionInfo

			#set upload dataset form 
			form = FileSearchForm()

			#rerender profile with information
			t = loader.get_template("profile.html")
			c = dict({"message": message, "sessionInfo" : sessionInfo, "folder": folder, "form": form})
			return HttpResponse(t.render(c, request=request)) 

		#if a request is made to download a dataset
		elif request.POST.get('downloadButton'):

			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')

			#set username, password, server and dataset 
			username = sessionInfo["username"]
			password = sessionInfo["password"]
			server = sessionInfo["server"]
			dataset = request.POST['dataset']

			#make request to api
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/download.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(dataset+'\n')

			#get response based on timeout function
			stdout,stderr,returncode = timeout(p)

			# set user message based on the process returncode 
			if returncode != 0: 
				message = dict({"value" : 'Error downloading dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "error"})
			else: 
				value = "Successfully Downloaded " + dataset
				message = dict({"value" : value, "type" : "success"}) 

			#rerender profile with information
			t = loader.get_template("profile.html")
			form = FileSearchForm()
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo, "form": form})
			return HttpResponse(t.render(c, request=request)) 

		#if request is made to launch a dataset
		elif request.POST.get('launchButton'):
			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')

			#set username, password, server and dataset 
			username = sessionInfo["username"]
			password = sessionInfo["password"]
			server = sessionInfo["server"]
			dataset = request.POST['dataset']
			version = request.POST['version']

			#make request to api
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/launch.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(dataset+'\n')
			p.stdin.write('\n')
			p.stdin.write(version+'\n')
			p.stdin.write('1\n')
			p.stdin.write('Base\n')

			#get response based on timeout function
			stdout,stderr,returncode = timeout(p)

			# set user message based on the process returncode 
			if returncode != 0: 
				message = dict({"value" : 'Error Launching dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "error"})
			else: 
				value = "Successfully launched " + dataset
				message = dict({"value" : value, "type" : "success"}) 

			#rerender profile with information
			form = FileSearchForm()
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo, "form": form})
			return HttpResponse(t.render(c, request=request)) 

		#if request is made to launch a dataset
		elif request.POST.get('uploadButton'):
			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')

			#set username, password, server and path to file 
			username = sessionInfo["username"]
			password = sessionInfo["password"]
			server = sessionInfo["server"]
			url = request.POST['url']

			#get dataset name and the location of that file
			absolute_path = os.path.abspath(url)
			index = absolute_path.rfind('\\')
			if index < 0: 
				index = absolute_path.rfind('/')
			location_folder = absolute_path[0: index]
			dataset = absolute_path[index+1:]


			#make request to api
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/upload.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(dataset+'\n')
			p.stdin.write(location_folder+'\n')

			#get response based on timeout function
			stdout,stderr,returncode = timeout(p)

			#add new dataset to user folder
			for line in stdout.splitlines(): 
				folder[dataset] = line

			# set user message based on the process returncode 
			if returncode != 0: 
				message = dict({"value" : 'Error Uploading dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "error"})
			else: 
				value = "Successfully Loaded " + dataset
				message = dict({"value" : value, "type" : "success"}) 
			
			#rerender profile with information
			form = FileSearchForm()
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo,"form": form})
			return HttpResponse(t.render(c, request=request)) 
		elif request.POST.get('queryButton'):
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo,"form": form})
			return HttpResponse(t.render(c, request=request)) 
		elif request.POST.get('graphButton'): 
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo,"form": form})
			return HttpResponse(t.render(c, request=request)) 


			