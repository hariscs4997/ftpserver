"""FDown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from MainApp.views import handle_camera1, handle_camera2, overview, impressum, login, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',handle_camera1, name='camera1'),
    path('camera2/',handle_camera2,name='camera2'),
    path('overview/',overview,name='overview'),
    path('impressum/',impressum,name='impressum'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
