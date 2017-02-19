from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork2 import views as socialnetwork_views

urlpatterns = [
    url(r'^$', socialnetwork_views.home, name='home'),
    #default page
    url(r'^global$', socialnetwork_views.home, name='global'),
    #follow a user
    #url(r'^follow$', socialnetwork_views.follow, name='follow'),
    #show all followers
    #url(r'^followstream$', socialnetwork_views.followstream, name='followstream'),
    #create new post
    url(r'^create$', socialnetwork_views.create, name='create'),
    #route to login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork2/login.html'}, name='login'),
    #logout
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    #route to profile page
    url(r'^profile$', socialnetwork_views.profile, name='profile'),
    url(r'^editprofile$', socialnetwork_views.editprofile, name='editprofile'),
    #route to register page
    url(r'^register$', socialnetwork_views.register, name='register')
]
