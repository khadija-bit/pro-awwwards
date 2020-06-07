from django import forms
from django.forms import ModelForm
from .models import Profile, Project, Review

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email')

class ProfileForm(ModelForm):
    class Meta:
        model = Project
        fields = ['profile_photo','user','bio','contact']

class ProjectForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['title','image','description','url']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['design','usability','content','overall_total']

