from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db import models

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

import inspect

# Create your views here.
@login_required
def home(request):
	all_info = []
	all_info = Messages.objects.values('user_id', 'post', 'date', 'user__last_name', 'user__first_name', 'user__username').order_by('-date')
	profile = Profile.objects.filter(user=request.user).values('user__last_name','user_id', 'user__first_name', 'user__username', 'age', 'bio','picture')
	print profile[0]['picture']
	context = {'messages': all_info, 'profile': profile[0]}
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
	if request.POST.get('username', False):
		if not 'username' in request.POST:
			print 'no user name'
			return render(request, 'socialnetwork/profile.html', {})

		username = request.POST['username']
		print 'get username'
		all_info = Messages.objects.filter(user__username=username).values('user_id', 'post', 'date', 'user__last_name', 'user__first_name', 'user__username').order_by('-date')
		context = {'messages': all_info}
		return render(request, 'socialnetwork2/profile.html', context)
	if request.POST.get('follow', False):
		follow = Follow()
		follow.user = request.user
		follow.follows = request.POST.get('followuser', False)
		follow.save()
		return redirect(reverse('home'))
	if request.POST.get('unfollow', False):
		followuser = request.POST.get('followuser', False)
		Follow.objects.filter(user=request.user).filter(follows=followuser).delete()
		return redirect(reverse('home'))


@login_required
def followstream(request):
	follows = Follow.objects.filter(user=request.user)
	following_message = Messages.objects.none()

	for p in follows:
		following_message1 = Messages.objects.filter(user__username=p.follows).values('user_id', 'post', 'date', 'user__last_name', 'user__first_name', 'user__username',)
	 	following_message = following_message | following_message1
	print following_message
	
	following_message = following_message.order_by('-date')
	
	profile = Profile.objects.filter(user=request.user).values('user__last_name','user_id', 'user__first_name', 'user__username', 'age', 'bio','picture')
	context = {'messages': following_message, 'profile': profile[0]}
	return render(request, 'socialnetwork2/followstream.html', context)

@login_required
@transaction.atomic
def editprofile(request):
	try:
		if request.method == 'GET':
			profile = Profile.objects.get(user=request.user)
			form = EditProfile(instance=profile)
			context = {'form': form}
			return render(request, 'socialnetwork2/editprofile.html', context)

		#profile = Profile.objects.select_for_update().get(user_id=request.user)
		profile = Profile.objects.select_for_update().get(user=request.user)
		form = EditProfile(request.POST, request.FILES, instance=profile)
		context = {}
		if not form.is_valid():
			context = {'form': form}
			return render(request, 'socialnetwork2/editprofile.html', context)
		else:
			print 'profile,', profile.content_type
			print 'form', type(3)
			try:
				if form.cleaned_data['picture'].content_type:
					profile.content_type = form.cleaned_data['picture'].content_type
			except:
				pass
			form.save()
			return redirect(reverse('home'))

	except Profile.DoesNotExist:
		return redirect(reverse('home'))

@login_required
def get_photo(request,id):
	user = get_object_or_404(User, id=id)
	return HttpResponse(user.profile.picture, content_type=user.profile.content_type)

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