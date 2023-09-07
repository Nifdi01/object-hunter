from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Image
        fields = ['image']
