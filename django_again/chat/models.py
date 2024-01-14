from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExclusiveRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    room_name = models.CharField(max_length=20)