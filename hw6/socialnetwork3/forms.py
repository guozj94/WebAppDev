from django import forms
from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=20, label='Username')
	first_name = forms.CharField(max_length=20, label='First Name')
	last_name = forms.CharField(max_length=20, label='Last Name')
	password1 = forms.CharField(max_length = 20, label='Password', widget = forms.PasswordInput())
	password2  = forms.CharField(max_length = 20, label='Confirm password', widget = forms.PasswordInput())

	"""docstring for RegistrationForm"""
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		return username

class EditProfile(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('age', 'bio', 'picture')

	def clean_profile(self):
		picture = self.cleaned_data['picture']
		if not picture:
			raise forms.ValidationError('You must upload a picture')
		if not picture.content_type or not picture.content_type.startswith('image'):
			raise forms.ValidationError('File type is not image')
		return picture