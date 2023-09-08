from django.shortcuts import render,get_object_or_404
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage
import os
from ultralytics import YOLO
from PIL import Image
from django.conf import settings
from .forms import ImageUploadForm
from .models import ObjectDetectionModel


def image_upload_view(request, pk):
    object_detection_model = get_object_or_404(ObjectDetectionModel, pk=pk)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image to the media directory
            uploaded_image = form.cleaned_data['image']
            fs = FileSystemStorage()
            image_path = fs.save(uploaded_image.name, uploaded_image)

            # Get the full path to the uploaded image
            image_full_path = os.path.join(fs.location, image_path)

            # Load the YOLO model associated with the selected detector
            yolo_model = YOLO(os.path.join(settings.MEDIA_ROOT, 'yolov8n.pt'))


            # Get the related CategoryLabel instance associated with the ObjectDetectionModel
            category_label = object_detection_model.category_label

            # Get the IDs of labels associated with the category_label
            class_ids = list(category_label.label_ids.values_list('label_id', flat=True))
            print(class_ids)

            # Perform object detection using the loaded model and class IDs
            results = yolo_model(image_full_path, classes=class_ids)



            # Process the results and save the annotated image
            for r in results:
                im_array = r.plot()  # Plot a BGR numpy array of predictions
                # Convert to RGB PIL image
                im = Image.fromarray(im_array[..., ::-1])
                annotated_image_path = os.path.join(
                    fs.location, 'annotated_' + uploaded_image.name)
                im.save(annotated_image_path)  # Save the annotated image

            os.remove(image_full_path)

            # Construct the URL for the annotated image
            annotated_image_url = os.path.join(
                settings.MEDIA_URL, 'annotated_' + uploaded_image.name)

            # Render the output image to the user
            context = {
                'results': results,
                'image': uploaded_image,
                'annotated_image_url': annotated_image_url,
                'selected_detector': object_detection_model,
                'form': form
            }
            return render(request, 'models/upload.html', context)

    # If the request is not a POST, render the form and pass the selected detector
    return render(request, 'models/upload.html', {'form': ImageUploadForm(), 'selected_detector': object_detection_model})



def list_models(request):
    # Retrieve all object detection models from the database
    models = ObjectDetectionModel.objects.all()
    context = {
        'models': models,
    }
    return render(request, 'models/model_list.html', context)
