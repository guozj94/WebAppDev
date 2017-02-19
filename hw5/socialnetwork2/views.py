from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

#import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

#import transaction
from django.db import transaction

#import models
from socialnetwork2.models import *

#import forms
from socialnetwork2.forms import *

#use time
from datetime import datetime
import time

from django.template import RequestContext

# Create your views here.
@login_required
def home(request):
	all_info = []
	all_info = Messages.objects.values('user_id', 'post', 'date', 'user__last_name', 'user__first_name', 'user__username')
	all_info.order_by('-date')
	profile = Profile.objects.filter(user=request.user).values('user__last_name', 'user__first_name', 'user__username', 'age', 'bio')
	#print profile
	context = {'messages': all_info, 'profile': profile[0]}
	print profile
	return render(request, 'socialnetwork2/global.html', context)

@login_required
def create(request):
	if not request.POST['input-content']:
		print 'no content'
	else:
		#create a new instance of Messages
		print 'create new content'
		message = Messages()
		message.user = request.user
		message.post = request.POST['input-content'][:200]
		message.save()
	return redirect(reverse('home'))

@login_required
def profile(request):
	if not 'username' in request.POST:
		print 'no user name'
		return render(request, 'socialnetwork/profile.html', {})

	#get the username
	username = request.POST['username']

	#search all posts posted by that user
	all_info = Messages.objects.filter(user__username=username).values('user_id', 'post', 'date', 'user__last_name', 'user__first_name', 'user__username')
	all_info.order_by('-date')
	context = {'messages': all_info}
	#print context
	return render(request, 'socialnetwork2/profile.html', context)

@login_required
def editprofile(request):
	try:
		if request.method == 'GET':
			profile = Profile.objects.get(user_id=request.user)
			form = EditProfile(instance=profile)
			context = {'form': form}
			return render(request, 'socialnetwork2/editprofile.html', context)

		profile = Profile.objects.select_for_update().get(user_id=request.user)
		form = EditProfile(request.POST, request.FILES, instance=profile)
		if not form.is_valid():
			context = {'form': form}
			return render(request, 'socialnetwork2/editprofile.html', context)
		else:
			profile.content_type = form.cleaned_data['picture'].content_type
			form.save()
			return redirect(reverse('home'))

	except Profile.DoesNotExist:
		return redirect(reverse('home'))
	# if request.method == 'GET':
	# 	context = {'form': EditProfile()}
	# 	return render(request, 'socialnetwork2/editprofile.html', context)

	# profile = Profile(user=request.user)
	# edit_profile = EditProfile(request.POST, instance=profile)
	# if not edit_profile.is_valid():
	# 	context = {'form': edit_profile}
	# 	return render(request, 'socialnetwork2/editprofile.html')
	# edit_profile.save()
	# return redirect(reverse('home'))

@transaction.atomic
def register(request):
	context = {}

	if request.method == "GET":
		context['form'] = RegistrationForm()
		return render(request, 'socialnetwork2/register.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'socialnetwork2/register.html', context)

	new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
	new_user.save()

	new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('home'))