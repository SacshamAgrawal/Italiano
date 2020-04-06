from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from django.conf import settings
from rest_framework import routers
import rest_framework

urlpatterns = [
    path('',include('pizza.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('api-auth/',include('rest_framework.urls')),
]+static( settings.MEDIA_URL , document_root= settings.MEDIA_ROOT )

if settings.DEBUG :
    import debug_toolbar
    urlpatterns = [
        path('__debug__',include(debug_toolbar.urls)),
    ]+urlpatterns