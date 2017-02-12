from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views as socialnetwork_views

urlpatterns = [
    url(r'^$', socialnetwork_views.home, name='home'),
    url(r'^global$', socialnetwork_views.home, name='global'),
    url(r'^create$', socialnetwork_views.create, name='create'),
    #url(r'^register$', socialnetwork_views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^profile$', socialnetwork_views.profile, name='profile'),
    url(r'^register$', socialnetwork_views.register, name='register')
]