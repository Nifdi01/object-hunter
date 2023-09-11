from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, ProfileRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from models.models import ModelUseCount, ObjectDetectionModel
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
from django.http import JsonResponse


#############
# API VIEWS #
#############


class ModelUseCountAPI(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile



##################
# STANDARD VIEWS #
##################


def landing_page(request):
    return render(request, 'account/landing_page.html')


@login_required
def user_dashboard(request):
    user_profile = request.user.profile
    model_use_count = user_profile.model_use_count

    # Extract labels and series from the JSON data
    labels = list(model_use_count.keys())
    series = list(model_use_count.values())
    
    # Calculate the most used model
    if len(model_use_count.items()) != 0:
        fav_model = sorted(model_use_count.items(), key=lambda x:x[1])[-1][0]
    else:
        fav_model = 'None'

    # Pass the data to the template
    context = {'section': 'dashboard', 'labels': labels, 'series': series, 'fav_model': fav_model}

    return render(request, 'account/dashboard.html', context)



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
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()  # Correctly initialize the ProfileRegistrationForm here
    
    return render(request, 'account/register.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def settings(request):
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
            
            return render(request, 'account/landing_page.html')
            
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/settings.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})