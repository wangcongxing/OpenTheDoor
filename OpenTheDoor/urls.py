"""OpenTheDoor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from app import views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from django.views import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 获取token
    # path('<str:version>/getAuthToken', views.LoginJWTAPIView.as_view(), name='getAuthToken'),
    url(r'^(?P<version>[v1|v2]+)/getAuthToken/', views.LoginJWTAPIView.as_view(), name='getAuthToken'),
    # 版本
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')
]
