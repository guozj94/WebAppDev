from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db import transaction

from socialnetwork.models import *

from datetime import datetime
import time

# Create your views here.
@login_required
#need query
def home(request):
	# messages = Messages.objects.all()
	# print messages

	# if messages.count() == 0:
	# 	return render(request, 'socialnetwork/global.html', {})

	# if messages.count() >= 1:
	# 	context = {'messages': messages.order_by('-date')}

	# return render(request, 'socialnetwork/global.html', context)
	all_info = []
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id ORDER BY socialnetwork_messages.date DESC'):
		#print p.first_name, p.last_name
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	print all_info[0]
	# while count_msg < messages.count():
	# 	while count_usr < user_info.count():
	# 		if messages[count_msg].user_id == user_info[count_usr].id:
	# 			messages[count_msg].fname = user_info[count_usr].first_name
	# 			messages[count_msg].lname = user_info[count_usr].last_name
	# 			messages[count_msg].username = user_info[count_usr].username
	# 		count_usr += 1
	# 	count_msg += 1
	# print user_info[0].first_name
	# print context
	context = {'messages': all_info}
	return render(request, 'socialnetwork/global.html', context)

@login_required
def create(request):
	if not 'input-content' in request.POST:
		return render(request, 'socialnetwork/global.html', {})

	message = Messages()
	message.user = request.user
	print request.user
	message.post = request.POST['input-content'][:200]
	message.save()
	all_info = []
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id ORDER BY socialnetwork_messages.date DESC'):
		#print p.first_name, p.last_name
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	print all_info[0]
	# while count_msg < messages.count():
	# 	while count_usr < user_info.count():
	# 		if messages[count_msg].user_id == user_info[count_usr].id:
	# 			messages[count_msg].fname = user_info[count_usr].first_name
	# 			messages[count_msg].lname = user_info[count_usr].last_name
	# 			messages[count_msg].username = user_info[count_usr].username
	# 		count_usr += 1
	# 	count_msg += 1
	# print user_info[0].first_name
	# print context
	context = {'messages': all_info}
	return render(request, 'socialnetwork/global.html', context)

@login_required
def profile(request):
	if not 'username' in request.POST:
		return render(request, 'socialnetwork/profile.html', {})

	username = request.POST['username']
	all_info = []
	for p in Messages.objects.raw('SELECT * FROM socialnetwork_messages,auth_user WHERE socialnetwork_messages.user_id=auth_user.id AND auth_user.username = %s ORDER BY socialnetwork_messages.date DESC', [username]):
		#print p.first_name, p.last_name
		all_info.append({'fname': p.first_name, 'lname': p.last_name, 'date': p.date, 'post': p.post, 'username': p.username})
	print all_info[0]
	context = {'messages': all_info}

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
