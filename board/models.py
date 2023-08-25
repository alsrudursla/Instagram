from django.db import models

from app01.models import Users


# Create your models here.
class Board(models.Model):
    contents = models.TextField()
    writer = models.CharField(max_length=30)
    bimg = models.ImageField(blank=True, upload_to="image")
    like = models.ManyToManyField(Users, related_name='like',blank = True)

class Comment(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    writer = models.ForeignKey(Users, on_delete=models.CASCADE)
    contents = models.TextField()