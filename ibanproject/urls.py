"""ibanproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from oauth.views import *
from ibanmanagment.views import DashBoardView, CreateIban, UpdateIban, DeleteIban, CommonCheck
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', AuthView.login, name='login'),
    url(r'^logout/$', AuthView.logout, name='logout'),
    url(r'^authlogin/$', AuthView.google_login, name='authlogin'),
    url(r'^$', AuthView.login, name='login'),
    url(r'^auth/complete/google-oauth2/$', AuthView.site_authentication, name='googleauthenticate'),
    url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
    url(r'^createiban/$', CreateIban.as_view(), {}, name='createiban'),
    url(r'^unique/iban/$', CommonCheck.checkuniqueiban, {}, name='uniqueiban'),
    url(r'^updateiban/(?P<pk>\d+)/$', UpdateIban.as_view(), {}, name='updateiban'),
    url(r'^deleteiban/(?P<pk>\d+)/$', DeleteIban.as_view(), {}, name='deleteiban'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Errors pages has been hanlded from here.
handler404 = 'oauth.views.not_found'
handler500 = 'oauth.views.server_error'
handler403 = 'oauth.views.permission_denied'
handler400 = 'oauth.views.bad_request'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    SHOW_TOOLBAR_CALLBACK = True