from django.shortcuts import render, redirect

from app01.models import Users, Follow
from board.models import Board

import bcrypt

from chat01.models import Room


# Create your views here.

def main(request):
    users = Users.objects.all()
    follow = Follow.objects.all()
    result = Board.objects.all().order_by('-id') #최신순으로 조회
    info = {"user" : users, "follow" : follow, "info" : result}
    return render(request,'index.html',info)

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        user_id = request.POST.get('user_id', None)
        user_pw = request.POST.get('user_pw', None)

        try:  # id 있을 때
            user = Users.objects.get(uname=user_id)
            if bcrypt.checkpw(user_pw.encode('utf-8'), user.password.encode('utf-8')):
                request.session['is_login'] = True
                request.session['user_id'] = user.uname
                request.session['user_uid'] = user.id
                return redirect('/')
        except Users.DoesNotExist:  # id 없을 때
            return redirect('/register/')

def logout(request):
    request.session['is_login'] = False
    return redirect('/')

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        user_id = request.POST.get('user_id', None)
        user_pw = request.POST.get('user_pw', None)
        user_img = request.FILES['user_img']

        new_password = user_pw.encode('utf-8')
        new_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password, new_salt)

        user = Users()
        user.uname = user_id
        user.password = hashed_password.decode('utf-8')
        user.uimg = user_img
        user.save()
        return redirect('/login/')

def profile(request):
    now_user = Users.objects.get(uname=request.session['user_id'])
    posting = Board.objects.all()
    info = {'user' : now_user, 'post' : posting}
    return render(request, "profile.html", info)

def new_profile(request,id):
    name = request.POST.get('user_id', None)
    pw = request.POST.get('user_pw', None)
    img = request.FILES['user_img']
    new_pw = pw.encode('utf-8')
    new_salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(new_pw, new_salt)

    edit_user = Users.objects.get(id=id)
    edit_user.uname = name
    edit_user.password = hashed_pw.decode('utf-8')
    edit_user.uimg = img
    edit_user.save()
    return redirect('/profile/')

def profile_edit(request, id):
    user = Users.objects.get(id=id)
    info = {"user" : user}
    return render(request, "profile_edit.html", info)

def follow(request, writer):
    try:
        following = Follow.objects.get(to_user=writer)
        if following.from_user == request.session['user_id']:
            return redirect('/chatroom/')
        else:
            me = request.session['user_id']
            you = Users.objects.get(uname=writer)

            follow = Follow()
            follow.from_user = me
            follow.to_user = you.uname
            follow.save()

            room = Room()
            room.room_number = request.session['user_uid'] + you.id
            room.from_user = me
            room.to_user = you.uname
            room.save()

            return redirect('/chatroom/')
    except Follow.DoesNotExist:
        me = request.session['user_id']
        you = Users.objects.get(uname = writer)

        follow = Follow()
        follow.from_user = me
        follow.to_user = you.uname
        follow.save()

        room = Room()
        room.room_number = request.session['user_uid'] + you.id
        room.from_user = me
        room.to_user = you.uname
        room.save()

        return redirect('/chatroom/')


def new_post(request):
    user = Users.objects.all()
    return render(request, "new_post.html", {"user" : user})