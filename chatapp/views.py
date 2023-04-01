from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from .models import Messange,Room
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
# Create your views here.
from django.http import HttpResponseBadRequest
def home(request):
    if request.method == "GET":
        return redirect('core:profile')
    if request.method == "POST":
        name = request.POST.get('name')
        if name!="":
            try:
                user_ = User.objects.get(username = name)
            except User.DoesNotExist:
                messages.success(request, "Tài khoảng không tồn tại")
                return redirect('chatapp:home')
            return render(request, 'chat/profile.html',{'user_':user_})
        else:
            messages.success(request, "bạn cần nhập tên tài khoảng bạn muốn tìm kiếm")
            return redirect('chatapp:home')
    
def messa(request,id):
    if request.method == "GET":
        user = request.user
        id2 = request.user.pk
        try:
            room = Room.objects.get(user_id1=id, user_id2=id2)
        except Room.DoesNotExist:
            try:
                room = Room.objects.get(user_id1=id2, user_id2=id)
            except Room.DoesNotExist:
                room = Room.objects.create(user_id1=id2, user_id2=id)
        try:
            mess = Messange.objects.filter(room=room)
            return render(request, 'chat/message.html', {'messages': mess,'room':room,'user':user})
        except Messange.DoesNotExist:
            mess = []
        return render(request, 'chat/message.html', {'messages': mess,'room':room,'user':user})



def send(request):
    username = request.user
    room_id = request.POST.get('room_id')
    message = request.POST.get('message')
    if room_id:
        room_id = int(room_id)
        # Retrieve the Room instance using the room_id string
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return HttpResponseBadRequest("Invalid room ID")
        if message!="":
            # Create the new message using the retrieved Room instance
            new_mess = Messange.objects.create(value=message, room=room, user=username)
            new_mess.save()
        else:
            return redirect('chapapp:message', id=room_id)
        
        return HttpResponse("Message sent successfully")
    
    # Add a default return statement
    return HttpResponseBadRequest("Invalid request")


def getMessages(request, id):
  
    room_details = Room.objects.get(id=id)
    username =[]
    messages = Messange.objects.filter(room=room_details)
    for i in messages:
        username.append(i.user.username)
    return JsonResponse({"messages":list(messages.values()),"user":username})