from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<int:id>/", views.room, name="room"),
    path("create-room/", views.create, name="form"),
    path("update-room/<int:id>/", views.update, name="update"),
    path("delete-room/<int:id>/", views.delete, name="delete"),
]