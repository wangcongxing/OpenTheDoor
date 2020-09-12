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
from django.urls import path, include
from app import views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from django.views import static
from rest_framework import routers

# 全自动路由
router = routers.DefaultRouter()
router.register(r'role', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
path('h/', views.h),
    # 自动生成增删改查url
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
    # 增删改查url配置
    url(r'^(?P<version>[v1|v2]+)/$', views.UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    url(r'^(?P<version>[v1|v2]+)/(?P<pk>\d+)/$', views.UserViewSet.as_view(
        {'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'partial_update'})),
    # 获取token
    # path('<str:version>/getAuthToken', views.LoginJWTAPIView.as_view(), name='getAuthToken'),
    url(r'^(?P<version>[v1|v2]+)/getAuthToken/', views.LoginJWTAPIView.as_view(), name='getAuthToken'),
    url(r'^(?P<version>[v1|v2]+)/getBossInfo/', views.GetBossInfo.as_view(), name='getBossInfo'),

    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')
]
