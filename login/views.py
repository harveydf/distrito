# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from login.forms import LoginForm

def login_user(request):
	if request.user.is_authenticated():	
		return HttpResponseRedirect('/')
	elif request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			form = LoginForm(auto_id=False)
			return render_to_response('login.jade', 
				{'form': form,
				'error': 'Usuario o contraseña incorrecta.'}, 
				context_instance=RequestContext(request))
	else:
		form = LoginForm(auto_id=False)
		return render_to_response('login.jade', {'form': form}, context_instance=RequestContext(request))