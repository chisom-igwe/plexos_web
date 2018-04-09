from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static
from plexos import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^logout/$', auth_views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
