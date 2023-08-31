from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_repeat = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        
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
    