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


def login(request): 
	"""
		This is the view that users see if they do not log into admin
		it colleges the user's information and send a sucess message 
	"""
	if request.method == "GET": 
		c = {}
		return render(request, "login.html",c)
	if request.method == "POST":
		user = authenticate(username= request.POST.get('username', ''), password = request.POST.get('password', ''))
		if user is None: 
			message = "Your information could not be found. Please contact Support at Energy Exemplar."
			t = loader.get_template('messages/error.html')
			c = dict({ 'message': message, })
			return HttpResponse(t.render(c,request=request))

		
@login_required
def profile(request):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	if request.method == "GET": 
		return render(request, "profile.html")
	elif request.method == "POST":
		if request.POST.get('connectButton'): 
			username = request.POST['username']
			password = request.POST['password']
			server = request.POST['server']
			message = ""
			userInfo = ""
			p = subprocess.Popen(['python2', os.path.join(SITE_ROOT + '../../Python-PLEXOS-API/Connect Server/connect.py')], stdin=subprocess.PIPE)
			p.stdin.write(server+'\n')
			p.stdin.write(username+'\n')
			p.stdin.write(password+'\n')
			stdout,stderr = p.communicate()
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
			c = dict({"message": message, "userInfo" : userInfo})
			return HttpResponse(t.render(c, request=request))