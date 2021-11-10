from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=75, required=True)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class UserForm(forms.ModelForm):
    num_visits = forms.CharField(max_length=1, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'num_visits')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth', 'megafaculty', 'group', 'info',)
