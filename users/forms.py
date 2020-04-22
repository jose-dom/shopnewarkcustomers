from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile, User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number','password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
