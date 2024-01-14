from django.shortcuts import render, redirect
from django.views.generic import View
from .models import ExclusiveRoom

# Create your views here.

class Room(View):
    def get(self, request, room_name):
        return render(request, "chat/room.html", {"room_name": room_name})

class CreateRoom(View):
    def get(self, request):


        return render(request, "chat/create_room.html")
        # return ren('chat:room', chat_room=room_name)
    
    def post(self, request):
        room_name = self.request.POST['room_name']
        new_room, c = ExclusiveRoom.objects.get_or_create(user1=self.request.user, user2=self.request.user, room_name=room_name)
        return redirect('chat:room', room_name=room_name)