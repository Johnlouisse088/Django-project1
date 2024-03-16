from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm   # for modifiacation of user form

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]        # password2 is a confirmation password

class RoomForm(ModelForm):
    class Meta:
        model = Room                # -> table name
        fields = '__all__'          # -> all fields from Room table at models.py (eg. host, topic, name, etc)
        exclude = ['host', 'participant'] # excluding data

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "username", "email", "bio"]

