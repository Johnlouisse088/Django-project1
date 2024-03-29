from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required       # for login verification
from django.contrib.auth.models import User                     # django-built in for user model
from django.contrib.auth.forms import UserCreationForm          # django-built in for user creation
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages                             # message
from django.db.models import Q                                  # -> You can use 'AND' or 'OR' logic
from .models import Room, Topic, Message, User
from .form import RoomForm, UserForm, MyUserCreationForm




# Create your views here.


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)  # Check if username and password exist in user admin
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
    form = MyUserCreationForm()                    # for registration of user from form.py
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)   # request.POST came from front-end (all data they filled)
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
    topics = Topic.objects.all()[:5]

    room_message = Message.objects.filter(
        Q(room__topic__name__icontains=query)
    )
    recent_messages = Message.objects.all()
    content = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_message": room_message,
        "recent_messages": recent_messages,
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

@login_required(login_url="login")
def room(request, id):

    room = Room.objects.all().get(id=id)
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
def profile_update(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES ,instance=user)        # request.file - receive from enctype in html file # use instance parameter to specify what the user profile will be update
        if form.is_valid():
            form.save()
            return redirect("profile", id=user.id)
    context = {
        "form": form
    }
    return render(request, "update-user.html", context)
@login_required(login_url="login")
def create(request):
    form = RoomForm()
    topics = Topic.objects.all()
    context = {
        "form": form,
        "topics": topics
    }
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topics, created = Topic.objects.get_or_create(name=topic_name)
        create_room = Room.objects.create(
            host = request.user,
            topic = topics,
            name = request.POST.get("name"),
            description = request.POST.get("description")
        )
        return redirect("home")
        # form = RoomForm(request.POST)  # -> create new  Room table!
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
            # form.save()                     # -> save() is like in model syntax
            # return redirect("home")         # -> the name from urls.py (eg. name="home")  # back to homepage

    return render(request, "room_form.html", context)


@login_required(login_url="login")
def update(request, id):

    room_id = Room.objects.get(id=id)
    form = RoomForm(instance=room_id)   # -> instance is use to specify the specific info of the data (get 1 row of data)
    topics = Topic.objects.all()
    if request.user != room_id.host:
        return HttpResponse("You're not allowed here!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room_id.topic = topic
        room_id.name = request.POST.get("name")
        room_id.description = request.POST.get("description")
        room_id.save()
        # form = RoomForm(request.POST, instance=room_id)  # use instance to update the specific data (without instance, you will create)
        # if form.is_valid():
        #     form.save()
        return redirect("home")

    context = {
        "form": form,
        "topics": topics
    }
    return render(request, "room_form.html", context)
@login_required(login_url="login")
def delete(request, id):

    room_id = Room.objects.get(id=id)
    if request.user != room_id.host:
        print("test", request.user.username, room_id.host.username)
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


def topicspage(request):
    query = request.GET.get('q') if request.GET.get ('q') is not None else ''
    topics = Topic.objects.filter(
        name__icontains = query
    )
    context = {
        "topics": topics
    }
    return render(request, "topics.html", context)

def activitiespage(request):
    rooms = Room.objects.all()[:3]
    context = {
        "rooms": rooms
    }
    return render(request, "activity.html", context)















