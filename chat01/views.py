from django.shortcuts import render

from app01.models import Users, Follow
from chat01.models import Room


# Create your views here.
def chat1(request):
    friends = Users.objects.all()
    to_user = Follow.objects.all()
    room_num = Room.objects.all()
    info = {"friends" : friends,
            "to" : to_user,
            "room_num" : room_num}

    return render(request,'chatroom.html',info)

def chat2(request, room_id, to_user):
    user = Users.objects.all()
    return render(request,'givechat.html', {'room_id' : room_id, "to" : to_user, 'user' : user})