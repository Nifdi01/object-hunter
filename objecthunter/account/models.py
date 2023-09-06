from django.db import models
from django.conf import settings

class Image(models.Model):
    image = models.ImageField(upload_to='images', blank=True)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default='defaults/userprofile.png', upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"