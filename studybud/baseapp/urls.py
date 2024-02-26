from django.urls import path,include
from . import views

urlpatterns = [
    path("login/", views.loginpage, name="login"),
    path("logout/", views.logoutpage, name="logout"),
    path("register/", views.registerpage, name="register"),
    path("", views.home, name="home"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path("room/<int:id>/", views.room, name="room"),
    path("create-room/", views.create, name="form"),
    path("update-room/<int:id>/", views.update, name="update"),
    path("delete-room/<int:id>/", views.delete, name="delete"),
    path("delete-message/<int:id>/", views.delete_message, name="delete_message"),
]