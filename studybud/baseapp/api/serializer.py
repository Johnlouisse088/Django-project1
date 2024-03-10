from rest_framework.serializers import ModelSerializer
from ..models import Room

class RoomsSerializer(ModelSerializer):          # to convert python objects to json format
    class Meta:
        model = Room
        fields = "__all__"

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"