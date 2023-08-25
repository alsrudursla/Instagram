"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import include

import app01.views
import chat01.views
import board.views
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', app01.views.main),
    #path('chatroom/', include('chat01.urls')),
    path('chatroom/', chat01.views.chat1),
    path('chatroom/<int:room_id>/<int:to_user>/', chat01.views.chat2),
    path('ws/chatroom/<int:room_id>/', chat01.views.chat2),

    path('login/', app01.views.login),
    path('logout/', app01.views.logout),
    path('register/', app01.views.register),
    path('profile/',app01.views.profile),
    path('profile/<int:id>/',app01.views.new_profile),
    path('profile_edit/<int:id>/', app01.views.profile_edit),
    path('follow/<str:writer>/', app01.views.follow),
    path('new_post/',app01.views.new_post),

    path('posting/', board.views.posting),
    path('del_post/<int:id>/<str:writer>/', board.views.del_post),
    path('edit_post/<int:id>/<str:writer>/', board.views.edit_post),
    path('edit_db/<int:id>/', board.views.edit_db),
    path('detail-page/<int:id>/', board.views.detail),
    path('like/<int:id>/', board.views.like),
    #path('create_comment/<int:id>/', board.views.create_comment),
    #path('show_comment/<int:id>/', board.views.show_comment),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
