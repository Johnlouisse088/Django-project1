from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Room
from .serializer import RoomsSerializer, RoomSerializer

@api_view(["GET"])
def getRoute(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/:id",
    ]
    return Response(routes)

@api_view(["GET"])
def getRooms(request):                                 # http://127.0.0.1:8000/api/rooms/
    rooms = Room.objects.all()
    serialized = RoomsSerializer(rooms, many=True)  # room = objects -> json  # many = when the data are more than one set it to True, but when the data is only one then set it to False
    return Response(serialized.data)

@api_view(["GET"])
def getRoom(request, id):                               # http://127.0.0.1:8000/api/rooms/<id>
    room = Room.objects.all().get(id=id)
    serialized = RoomSerializer(room, many=False)
    return Response(serialized.data)