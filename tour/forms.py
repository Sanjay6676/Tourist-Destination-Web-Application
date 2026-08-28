from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Destinations, DestinationImages
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the email id',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Confirm the password',
    }))

    class Meta:
        model= User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        
class ProfileForm(forms.ModelForm):
    f_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the First name'
    }))

    l_name=forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the last name'
    }))

    contact_no = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter the contact number'
    }))

    class Meta:
        model = Profile
        fields = [
            'f_name',
            'l_name',
            'contact_no'
        ]

class DestinationImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control'
    }))

    review = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Reviews here....'
    }))
    
    class Meta:
        model = DestinationImages
        fields = [
            'image',
            'review',
        ]

