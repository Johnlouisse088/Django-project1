from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser  # to modify user model

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    # models.ForeignKey() -> Many to one relationship
    # models.ManyToMany() -> Many to Many relationship
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)       # when User table got deleted the host data will set to Null
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)     # Cascade - when User table got deleted the host data will delete too
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    participant = models.ManyToManyField(User, related_name="participants", blank=True)   # models.ManyToManyField(<Tablename>,<name use in views.py>, it's okay to get an empty value in participants) # related_name = name in admin panel
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-updated", "-created"]         # with '-' is descending order (last will be the first)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                # -> foreignkey is to connect another table
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)    # model.key -> the Room table is the 'parent' and the Message table is the 'child'
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[:50]