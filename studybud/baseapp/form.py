from django.forms import ModelForm
from .models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model = Room                # -> table name
        fields = '__all__'          # -> all fields from Room table at models.py (eg. host, topic, name, etc)
        exclude = ['host', 'participant'] # excluding data



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
