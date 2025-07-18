"""
URL configuration for auto_writer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",main_views.incoming_message,name="home"),
    path("options",main_views.additional_options,name="options"),
    path("get-clip-board",main_views.get_last_copied_text,name="get_clip_board"),
    path("take-screen-shot",main_views.take_screen_shot,name="take_screen_shot")
]
