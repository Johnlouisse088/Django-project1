from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)       # when User table got deleted the host data will set to Null
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)     # Cascade - when User table got deleted the host data will delete too
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # participant =
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

    def __str__(self):
        return self.body[:50]