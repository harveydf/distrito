from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required(login_url='login/')
def home(request):
	return render_to_response('index.jade',{'test': 'Holaa', 'username': request.user.username})
