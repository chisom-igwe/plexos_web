# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import FileExtensionValidator
from django.db import models
from django import forms
from common import file_size

# Create your models here.

# Change Passowrd to make it more secure

class UserInfo(models.Model): 
	Server = models.CharField(max_length=10)
	Username = models.CharField(max_length=35)
	Password = models.CharField(max_length=35)

	@classmethod
	def create(cls, server, username, password): 
		user = cls(Server = server, Username = username, Password=password)
		user.save()
		return user

class Source_File(models.Model): 
	url = models.FileField(upload_to='files\%H\%M\%S',  validators=[FileExtensionValidator(allowed_extensions=['xml']), file_size])
