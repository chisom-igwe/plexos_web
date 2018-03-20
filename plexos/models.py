# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

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

 