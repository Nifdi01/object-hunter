from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from models.models import ObjectDetectionModel, ModelUseCount

@receiver(post_save, sender=User)
def initialize_model_use_counts(sender, instance, created, **kwargs):
    if created:
        # Get all object models
        object_models = ObjectDetectionModel.objects.all()

        # Initialize use counts for each object model to zero for the new user
        for model in object_models:
            ModelUseCount.objects.create(user=instance, model=model, count=0)
