from django.db import models

# Create your models here.
class Room(models.Model):
    room_number = models.IntegerField()
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)


class Chatting(models.Model):
    room_id = models.IntegerField()
    message = models.TextField()
    to = models.IntegerField()
    from_user = models.IntegerField()
