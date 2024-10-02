"""
URL configuration for shalil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Movie.views import play_video, upload_video, video_list, stream_video,index
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path("", index, name ="index" ),
    path("upload/", upload_video, name ="upload_video" ),
    path('videos/', video_list, name='video_list'),
    path('videos/play/<str:video_name>/', stream_video, name='play_video'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)