from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.


def home(request):
    rooms = Room.objects.all()
    content = {"rooms": rooms}
    return render(request, "home.html", content)


def room(request, id):
    rooms = Room.objects.values()
    room = Room.objects.get(id=id)
    context = {"dict1": room}
    return render(request, "room.html", context)
