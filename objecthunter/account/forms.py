from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'age']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected the call to super()
        self.fields['photo'].widget.attrs['class'] = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
        self.fields['gender'].widget.attrs['class'] = "block p-1 w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
        self.fields['age'].widget.attrs['class'] = "block p-1 w-20 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_repeat = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Passwords do not match!')
        return cd['password_repeat']
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
        
    def clean_email(self):
        target = self.cleaned_data
        if User.object.exclude(id=self.instance.id).filter(email=target).exists():
            raise forms.ValidationError('Email Already in use!')
        return target
    

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
    