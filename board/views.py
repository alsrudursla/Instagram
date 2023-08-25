from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from app01.models import Users
from board.models import Board, Comment


# Create your views here.
def posting(request):
    contents = request.POST.get('contents',None)
    bimg = request.FILES['image']

    post = Board()
    post.contents = contents
    post.bimg = bimg
    post.writer = request.session['user_id']
    post.save()

    return redirect('/')

def del_post(request, id, writer):
    now_user = Users.objects.get(uname=writer)
    post = Board.objects.get(id=id)
    if now_user.uname == request.session['user_id']:
        post.delete()
        return redirect('/')
    else :
        #경고 알림창 넣고 싶은데ㅠ
        return redirect('/')

def edit_post(request, id, writer):
    now_user = Users.objects.get(uname=writer)
    post = Board.objects.get(id=id)
    info = { "user" : now_user, "info" : post }
    if now_user.uname == request.session['user_id']:
        return render(request, 'edit_post.html', info)
    else :
        return redirect('/')

def edit_db(request, id):
    contents = request.POST.get('contents',None)

    post = Board.objects.get(id=id)
    post.contents = contents
    post.save()
    return redirect('/')

def detail(request, id):
    now_user = Users.objects.get(uname = request.session['user_id'])
    posting = Board.objects.get(id=id)
    info =  {"user": now_user, "info" : posting}
    return render(request,'detail-page.html', info)

def like(request, id):
    board = Board.objects.get(id=id)
    user = Users.objects.get(uname=request.session['user_id'])

    if board.like.filter(id=user.id).exists():
        board.like.remove(user)
        message = "del like"
    else:
        board.like.add(user)
        message = "add like"

    return JsonResponse({
        "message" : message
    })

'''
def create_comment(request, id):
    comment = Comment()
    comment.board_id = Board.objects.get(id=id).id
    comment.writer = request.session['user_id']
    comment.contents = request.POST.get('contents',None)
    comment.save()
    return redirect('/show_comment/'+ id +'/')

def show_comment(request, id):
    comment = Comment.objects.filter(board_id=id)
    info = {"info" : comment}
    return 
'''
