from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required       # for login verification
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages                             # message
from django.db.models import Q                                    # -> You can use 'AND' or 'OR' logic
from .models import Room, Topic, Message
from .form import RoomForm




# Create your views here.


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Check if username and password exist in user admin
        if user is not None:
            login(request, user)                # -> it will create a session id in cookies (inspect > application)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")


    page = "login"
    context = {
        "ispage": page
    }
    return render(request, "loginpage.html", context)

def registerpage(request):
    form = UserCreationForm()                    # for registration of user
    if request.method == "POST":
        form = UserCreationForm(request.POST)   # request.POST came from front-end (all data they filled)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "MORON!")


    page = "register"
    context = {
        "ispage": page,
        "form": form
    }

    return render(request, "loginpage.html", context )
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

    room_message = Message.objects.filter(
        Q(room__topic__name__icontains=query)
    )
    content = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_message": room_message
    }
    return render(request, "home.html", content)

def profile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "topics": topics,
        "room_message": room_message
    }
    return render(request, "profile.html", context)


def room(request, id):

    room = Room.objects.get(id=id)
    room_message = room.message_set.all()           # <parent_table>.<child_talbe(lowecase)>.message_set.all() -> call all data from child table which is the message (many to one)
    room_participants = room.participant.all()      # get the child of Room (id is equal to 1)
    if request.method == "POST":
        create_message = Message.objects.create(    # create data to Message table
            user = request.user,
            room = room,
            body = request.POST.get("body")        # the 'body' is from the html attribute with the name of 'name' // like in dictionary, you need to call the key first before you access the value
        )
        room.participant.add(request.user)          # add in participant attribute. (The arguiment are whole information of the user, NOT only the name!)
        return redirect("room", id=room.id)     # you need to pass the 2 arguiments becuase it is the requirement in url > function (room)

    context = {
        "room": room,
        "room_messages": room_message,
        "room_participants": room_participants
    }
    return render(request, "room.html", context)

@login_required(login_url="login")
def create(request):
    form = RoomForm()
    context = {"form": form}
    if request.method == "POST":
        form = RoomForm(request.POST)       # -> create new  Room table!
        if form.is_valid():
            form.save()                     # -> save() is like in model syntax
            return redirect("home")         # -> the name from urls.py (eg. name="home")  # back to homepage
    return render(request, "room_form.html", context)

@login_required(login_url="login")
def update(request, id):

    room_id = Room.objects.get(id=id)
    form = RoomForm(instance=room_id)   # -> instance is use to specify the specific info of the data (get 1 row of data)

    if request.user != room_id.host:
        return HttpResponse("You're not allowed here!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room_id)  # use instance to update the specific data (without instance, you will create)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "room_form.html", context)
@login_required(login_url="login")
def delete(request, id):

    room_id = Room.objects.get(id=id)
    if request.user != room_id.host:
        return HttpResponse("You're not allowed here!")
    if request.method == "POST":
        room_id.delete()
        return redirect("home")
    context = {"room": room_id}
    return render(request, "delete.html", context)


@login_required(login_url="login")
def delete_message(request, id):

    room_id = Message.objects.get(id=id)
    if request.method == "POST":
        room_id.delete()
        return redirect("home")
    context = {
        "room": room_id
    }

    return render(request, "delete.html", context)
















