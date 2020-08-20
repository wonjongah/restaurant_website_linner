from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
    intro = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = ['nickname', 'intro', 'phone', 'photo']
