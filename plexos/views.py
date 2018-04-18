# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import (authenticate, login as auth_login) 
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .common import *
from .models import *
from .forms import *
import subprocess
import re, os, shutil
from os import path, listdir
from os.path import abspath, dirname, isfile, join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Create your views here.

'''
	This is the view to login into the application 
	It asks for a users username and password 
	and redirects them to the profile page if logged in 
	or sends back to login page if there is an error
'''

def home(request): 
	if request.method == 'GET':
		return HttpResponseRedirect("/login/")
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


		
def profile(request):
	if request.method == "GET": 
		if not request.user.is_authenticated():
			return HttpResponseRedirect("/login/")
		return render(request, "profile.html")
	elif request.method == "POST":
		if request.POST.get('connectButton'):
			#Get user defined values for username, password, server 
			username = request.POST['username']
			password = request.POST['password']
			server = request.POST['server']
			form = FileSearchForm()

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
				message = dict({"value" : 'Error Connecting to server. Ensure that you entered the corrent server, username and password. Please try again', "type" : "danger"})
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
			sessionInfo = dict({"username": username, "password": password, "server": server, "solution_files": False, "connect":True})
			request.session['sessionInfo'] = sessionInfo


			#rerender profile with information
			t = loader.get_template("profile.html")
			c = dict({"message": message, "sessionInfo" : sessionInfo, "folder": folder, 'form': form})
			return HttpResponse(t.render(c, request=request)) 

		#if a request is made to download a dataset
		elif request.POST.get('downloadButton'):
			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')
			form = FileSearchForm()

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
				message = dict({"value" : 'Error downloading dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "danger"})
			else: 
				value = "Successfully Downloaded " + dataset
				message = dict({"value" : value, "type" : "success"}) 

			#rerender profile with information
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo, 'form': form})
			return HttpResponse(t.render(c, request=request)) 

		#if request is made to launch a dataset
		elif request.POST.get('launchButton'):
			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')
			form = FileSearchForm()

			#set username, password, server and dataset 
			username = sessionInfo["username"]
			password = sessionInfo["password"]
			server = sessionInfo["server"]
			dataset = request.POST['dataset']
			version = request.POST['version']
			runIndex = ''

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


			for line in stdout.splitlines():
				if 'Run' in line: 
					runIndex = re.findall(r'Run (.*?) is complete.', line, re.DOTALL)

			if runIndex != '': 
				#make request to api
				dp = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Solution Files/download.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				dp.stdin.write(server+'\n')
				dp.stdin.write(username+'\n')
				dp.stdin.write(password+'\n')
				dp.stdin.write(runIndex[0]+'\n')
				stdout_dp,stderr_dp,returncode_dp = timeout(dp)

				# set user message based on the process returncode 
				if returncode_dp != 0: 
					message = dict({"value" : 'Error Getting Solution Files. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "danger"})
				else: 
					value = "Successfully launched " + dataset
					message = dict({"value" : value, "type" : "success"}) 
			else: 
				message = dict({"value" : 'Error Launching dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "danger"})
			#rerender profile with information
			sessionInfo["solution_files"] = True; 
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo, 'form': form})
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
			location_folder= os.path.join(BASE_DIR, 'static','media').replace('\\', '/')
			dataset=''

			form = FileSearchForm(request.POST, request.FILES)
			if form.is_valid(): 
				initial_obj = form.save(commit=False)
				initial_obj.save()
				location_folder += str('/' + str(initial_obj.url)) 
				index = location_folder.rfind('/')
				path = location_folder[0:index+1]
				dataset = location_folder[index+1:]
				form.save()

				parseXMLResults = parseXML(location_folder)
				if not parseXMLResults: 
				#make request to api
					p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/upload.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					p.stdin.write(server+'\n')
					p.stdin.write(username+'\n')
					p.stdin.write(password+'\n') 
					p.stdin.write(username+'\n')
					p.stdin.write(dataset+'\n') 
					p.stdin.write(path+'\n')


					#get response based on timeout function
					stdout,stderr,returncode = timeout(p)


					# set user message based on the process returncode 
					if returncode != 0: 
						message = dict({"value" : 'Error Uploading dataset. Please try again. If the problem persists, contact support at Energy Exemplar', "type" : "danger"})
					else: 
						for line in stdout.splitlines(): 
							if "new_version" in line:  
								folder[dataset] = re.findall(r'version (.*?)$', line, re.DOTALL)
							request.session['folder'] = folder
						value = "Successfully Loaded " + dataset
						message = dict({"value" : value, "type" : "success"})
					
				else: 
					message = dict({"value" : parseXMLResults, "type" : "danger"})
			else: 
				# Get the validation errors of the uploaded files 
				form_errors = ""
				for key, value in form.errors.iteritems(): 
					form_errors += re.sub('<[^>]*>', '', str(value)).replace("&#39;", "\"")
				message = dict({"value" : form_errors, "type" : "danger"})

			#rerender profile with information
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo, 'form':form})
			return HttpResponse(t.render(c, request=request))

		#if request is made to download a dataset
		elif request.POST.get('downloadSolutionButton'):

			#get session folder and user information
			folder = request.session.get('folder')
			sessionInfo = request.session.get('sessionInfo')
			pandas_returncode = ''
			squalite_returncode = ''


			#initalize the return message to the user 
			message = dict({"value": "", "type":""});
			
			#if the user request for a sqlite solution file
			if request.POST.get('sqlite_solution'): 
				#make request to api for sqlite solution and get response 
				p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/query_to_sqlite3.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				stdout,stderr,squalite_returncode = timeout(p)
				
				#respond based on the returncode 
				if squalite_returncode != 0: 
					message["value"] = 'Error Downloading Solution in Sqlite Format. Please try again. If the problem persists, contact support at Energy Exemplar\n\n'
				else: 
					message["value"] = "Successfully downloaded solution in sqlite3 format\n"

			#if the user request for a pandas solution file
			if request.POST.get('pandas_solution'): 

				#make request to api for pandas solution and get response 
				p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/query_to_pandas.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				stdout,stderr,pandas_returncode = timeout(p)

				#respond based on the returncode
				if pandas_returncode != 0: 
					message["value"] += 'Error Downloading Solution in Pandas Format. Please try again. If the problem persists, contact support at Energy Exemplar'
				else: 
					message["value"] += "Successfully downloaded solution in sqlite3 format"

			if squalite_returncode != 0 and pandas_returncode != 0: 
				message["type"] = "success"
			elif squalite_returncode != 0 or pandas_returncode != 0:
				message["type"] = "info"
			else: 
				message["type"] = "danger"


			#rerender profile.html with information
			t = loader.get_template("profile.html")
			c = dict({"message": message,"folder": folder,"sessionInfo" : sessionInfo})
			return HttpResponse(t.render(c, request=request)) 


			