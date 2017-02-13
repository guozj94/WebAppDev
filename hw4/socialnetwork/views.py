from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

#import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

#import transaction
from django.db import transaction

#import model
from socialnetwork.models import *

#use time
from datetime import datetime
import time

# Create your views here.
@login_required
#display all posts on the home page
def home(request):
	all_info = []
	#join query
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id ORDER BY socialnetwork_messages.date DESC'):
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	#return messages and insert into html
	context = {'messages': all_info}
	return render(request, 'socialnetwork/global.html', context)

@login_required
#create new post, and render the homepage
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

	#get all post in database
	all_info = []
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id ORDER BY socialnetwork_messages.date DESC'):
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	
	#return messages and insert into html
	context = {'messages': all_info}
	return render(request, 'socialnetwork/global.html', context)

@login_required
#display user's profile
def profile(request):
	if not 'username' in request.POST:
		return render(request, 'socialnetwork/profile.html', {})

	#get the username
	username = request.POST['username']

	#search all posts posted by that user
	all_info = []
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id AND auth_user.username = %s ORDER BY socialnetwork_messages.date DESC', [username]):
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	
	#return messages and insert into html
	context = {'messages': all_info, 'lname': all_info[0]['lname'], 'fname': all_info[0]['fname'], 'totalpost': len(all_info)}
	return render(request, 'socialnetwork/profile.html', context)


@transaction.atomic
def register(request):
	context = {}
	errors = []
	context['errors'] = errors

	if request.method == 'GET':
		return render(request, 'socialnetwork/register.html', context)

	if not 'username' in request.POST or not request.POST['username']:
		errors.append('Username is required.')
	else:
		context['username'] = request.POST['username']

	if not 'lname' in request.POST or not request.POST['lname']:
		errors.append('Last name is required.')
	else:
		context['lname'] = request.POST['lname']

	if not 'fname' in request.POST or not request.POST['fname']:
		errors.append('First name is required.')
	else:
		context['fname'] = request.POST['fname']

	if not 'password1' in request.POST or not request.POST['password1']:
		errors.append('Password is required.')
	if not 'password2' in request.POST or not request.POST['password2']:
		errors.append('Confirm password is required.')

	if errors:
		return render(request, 'todolist2/register.html', context)

	if request.POST['password1'] != request.POST['password2']:
		errors.append('Passwords did not match.')

	if User.objects.select_for_update().filter(username = request.POST['username']).exists():
		errors.append('Username is already taken.')

	if errors:
		return render(request, 'register.html', context)

	new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], first_name=request.POST['fname'], last_name=request.POST['lname'])
	new_user.save()

	new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])

	login(request, new_user)
	return redirect(reverse('home')) #redirect to dict
