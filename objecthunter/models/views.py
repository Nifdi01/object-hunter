from django.shortcuts import render
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage
import os
from ultralytics import YOLO
from PIL import Image
from django.conf import settings
from .forms import ImageUploadForm
# from .models import ObjectDetectionModel

def image_upload_view(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ImageUploadForm(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            # Save the uploaded image to the media directory
            uploaded_image = form.cleaned_data['image']
            fs = FileSystemStorage()
            image_path = fs.save(uploaded_image.name, uploaded_image)

            # Get the full path to the uploaded image
            image_full_path = os.path.join(fs.location, image_path)

            # Perform object detection using YOLO
            model = YOLO("objecthunter/media/yolov8n.pt")  # Load the pretrained YOLOv8n model
            results = model(image_full_path, classes=[0,1])  # Perform inference

            # Process the results and save the annotated image
            for r in results:
                im_array = r.plot()  # Plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # Convert to RGB PIL image
                annotated_image_path = os.path.join(fs.location, 'annotated_' + uploaded_image.name)
                im.save(annotated_image_path)  # Save the annotated image

            os.remove(image_full_path)
            
            # Construct the URL for the annotated image
            annotated_image_url = os.path.join(settings.MEDIA_URL, 'annotated_' + uploaded_image.name)

            # Render the output image to the user
            context = {
                'results': results,
                'image': uploaded_image,
                'annotated_image_url': annotated_image_url,
            }
            return render(request, 'models/upload.html', context)

    # If the request is not a POST, render the form
    return render(request, 'models/upload.html', {'form': ImageUploadForm()})



def list_models(request):
    # Retrieve all object detection models from the database
    models = ObjectDetectionModel.objects.all()
    context = {
        'models': models,
    }
    return render(request, 'models/model_list.html', context)

