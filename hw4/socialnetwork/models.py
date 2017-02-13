from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#Message class saves all post message
class Messages(models.Model):
	user = models.ForeignKey(User, default=None)
	post = models.TextField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'user=' + str(self.id) + ',post="' + self.post + '"'
# Create your models here.
