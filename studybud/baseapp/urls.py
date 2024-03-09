from django.urls import path,include
from . import views

urlpatterns = [
    path("login/", views.loginpage, name="login"),
    path("logout/", views.logoutpage, name="logout"),

    path("register/", views.registerpage, name="register"),
    path("", views.home, name="home"),
    path("room/<int:id>/", views.room, name="room"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path("update_profile/<int:id>/", views.update_profile, name="update"),

    path("create-room/", views.create, name="form"),
    path("update-room/<int:id>/", views.update, name="update"),
    path("delete-room/<int:id>/", views.delete, name="delete"),
    path("delete-message/<int:id>/", views.delete_message, name="delete_message"),

    path("more-topics/", views.topic_page, name="topic_page"),
    path("recent-activities/", views.activity_page, name="topic_page"),

]