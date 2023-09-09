from django.db import models
import os
from ultralytics import YOLO
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(upload_to='images', blank=True)

class LabelID(models.Model):
    label_id = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.label_id)

class CategoryLabel(models.Model):
    label_name = models.CharField(max_length=255)
    label_ids = models.ManyToManyField(LabelID, related_name='category_labels')

    def __str__(self):
        return self.label_name

class ObjectDetectionModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    model_file = models.FileField(upload_to='')
    classes_during_inference = models.ManyToManyField(CategoryLabel, related_name='models_inference', blank=True)
    category_label = models.ForeignKey(CategoryLabel, on_delete=models.CASCADE, related_name='model', default=1)

    def __str__(self):
        return self.title


class ModelUseCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(ObjectDetectionModel, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.model.title} - {self.count} uses'