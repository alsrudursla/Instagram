from django.db import models

# Create your models here.
class Users(models.Model):
    uname = models.CharField(max_length=30)
    password = models.TextField()
    uimg = models.ImageField(blank=True)

class Follow(models.Model):
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)
