from django.db import models
from django.conf import settings
from models.models import ObjectDetectionModel

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default='defaults/userprofile.png', upload_to='users/%Y/%m/%d/', blank=True)
    model_use_count = models.JSONField(default=dict)  # Store use count for each model as a JSON dictionary

    def __str__(self):
        return f"Profile of {self.user.username}"
