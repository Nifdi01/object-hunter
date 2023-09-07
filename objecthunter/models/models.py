from django.db import models

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
    category_labels = models.ManyToManyField(CategoryLabel, related_name='models')
    classes_during_inference = models.ManyToManyField(CategoryLabel, related_name='models_inference', blank=True)
    # Add other fields as needed, e.g., model_file, created_at, updated_at, etc.

    def __str__(self):
        return self.title
