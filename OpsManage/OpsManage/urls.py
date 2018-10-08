"""devops1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.login_view),
    url(r'^loginSubmit$',views.loginSubmit),
    url(r'^logout$',views.logout_view),
    url(r'^accounts/', include('accounts.urls')),
    url('^cmdb/', include(('cmdb.urls', 'cmdb'), namespace='cmdb')), #django2.0必须在include里面加上应用的名字
    url(r'^search/', include(('haystack.urls', 'haystack'), namespace='haystack')),
    url(r'^wiki/', include(('wiki.urls', 'wiki'), namespace='wiki')),
    url(r'^api/', include(('api.urls', 'api'), namespace='api')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)