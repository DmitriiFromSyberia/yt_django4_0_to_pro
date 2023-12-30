from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # name = models.CharField(max_length=100)
    # price = models.IntegerField()
    # description = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to="_profile_images")
    contact_number = models.CharField(max_length=50, default="+18889225632")

    def __str__(self):
        return self.user.username
