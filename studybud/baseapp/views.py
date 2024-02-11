from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q              # -> You can use 'AND' or 'OR' logic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .form import RoomForm




# Create your views here.


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("test", username)
        print("test", password)

        user = authenticate(request, username=username, password=password)  # Check if username and password exist in user admin
        if user is not None:
            login(request, user)                # -> it will create a session id in cookies (inspect > application)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")



    context = {}
    return render(request, "loginpage.html", context)

def logoutpage(request):
    logout(request)                         # -> it will delete a session id in cookies (inspect > application)
    return redirect("home")

def home(request):
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
            # request.GET.get('q') -> http://127.0.0.1:8000/?q=Python    (get the 'Python')
    # rooms = Room.objects.filter(topic__name__icontains=query)   # icontains/contains(case sensitive)  # '' means all contains
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |                         # -> OR logic gate
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    room_count = rooms.count()

    topics = Topic.objects.all()
    content = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count
    }
    return render(request, "home.html", content)


def room(request, id):
    rooms = Room.objects.values()
    room = Room.objects.get(id=id)
    context = {"dict1": room}
    return render(request, "room.html", context)


def create(request):
    form = RoomForm()
    context = {"form": form}
    if request.method == "POST":
        form = RoomForm(request.POST)       # -> create new  Room table!
        if form.is_valid():
            form.save()                     # -> save() is like in model syntax
            return redirect("home")         # -> the name from urls.py (eg. name="home")  # back to homepage
    return render(request, "room_form.html", context)


def update(request, id):
    room_id = Room.objects.get(id=id)
    form = RoomForm(instance=room_id)   # -> instance is use to specify the specific info of the data (get 1 row of data)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room_id)  # use instance to update the specific data (without instance, you will create)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "room_form.html", context)

def delete(request, id):
    room_id = Room.objects.get(id=id)
    if request.method == "POST":
        room_id.delete()
        return redirect("home")
    context = {"room": room_id}
    return render(request, "delete.html", context)
















