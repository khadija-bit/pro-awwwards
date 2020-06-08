from django import forms
from django.forms import ModelForm
from .models import Profile, Project, Review
from django.contrib.auth.models import User
class SignInForm(forms.Form):
    your_name = forms.CharField(max_length=30)
    email = forms.EmailField(label='Email')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio')

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields = ('title', 'description', 'image', 'url')

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('design', 'usability', 'content')
