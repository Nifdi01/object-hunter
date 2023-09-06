from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ProfileRegistrationForm, ImageUploadForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage
import os
from ultralytics import YOLO
from PIL import Image
from django.conf import settings

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
            results = model(image_full_path)  # Perform inference

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
            return render(request, 'account/upload.html', context)

    # If the request is not a POST, render the form
    return render(request, 'account/upload.html', {'form': ImageUploadForm()})






def landing_page(request):
    return render(request, 'account/landing_page.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    
    return render(request,
                    'account/register.html',
                    {'user_form': user_form, 'profile_form':profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})