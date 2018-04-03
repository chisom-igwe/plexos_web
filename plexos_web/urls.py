from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from plexos import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^logout/$', auth_views.logout, name='logout'),


]
