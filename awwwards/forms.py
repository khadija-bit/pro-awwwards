from django import forms
from django.forms import ModelForm
from .models import Profile, Project, Review

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectForm(ModelForm):
    class Meta:
        model=Profile
        fields = '__all__'

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['design', 'usability', 'content', 'overall_total']

