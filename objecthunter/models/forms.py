from django import forms
from .models import ObjectDetectionModel

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    # selected_detector = forms.ModelChoiceField(
    #     queryset=ObjectDetectionModel.objects.all(), empty_label=None
    # )