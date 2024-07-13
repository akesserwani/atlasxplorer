from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#main map model
class UserMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usermap", null=True)

    name = models.CharField(max_length=50)
    private = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name 

class Pin(models.Model):
    usermap = models.ForeignKey(UserMap, on_delete=models.CASCADE, related_name="pin")

    name = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.name 


