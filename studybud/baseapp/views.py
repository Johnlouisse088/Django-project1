from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .form import RoomForm


# Create your views here.

def loginpage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "error.html", context)

    return render(request, "login.html", context)

def logoutpage(request):
    logout(request)
    return redirect("home")

def home(request):
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
            # request.GET.get('q') -> http://127.0.0.1:8000/?q=Python    (get the 'Python')
    print("test", query)
    rooms = Room.objects.filter(topic__name__icontains=query)   # icontains/contains(case sensitive)  # '' means all contains
    topics = Topic.objects.all()
    count_room = rooms.count()
    content = {
        "rooms": rooms,
        "topics": topics,
        "room_count": count_room
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
















