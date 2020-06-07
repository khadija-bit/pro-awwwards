from django.shortcuts import render,redirect
from .models import Profile, Project, Review
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import SignInForm,ProfileForm, ProjectForm,ReviewForm

# Create your views here.
def index(request):
    projects = Project.objects.all()
    profile = Profile.objects.all()
    return render(request,'index.html',{"projects":projects})

def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
       search_term = request.GET.get("project")
       searched_projects = Project.search_projects(search_term)

       message = f"{search_term}"

       return render(request, 'search.html',{"message":message, "projects": searched_projects})
    else:
        message = "You haven't searched for any term "
        return render(request, 'search.html',{"message":message})   

def profile(request):
    return render(request, 'profile.html')

def new_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('index')
        else:
            form = ProfileForm()
    return render(request, 'new_profile.html',{"form":form})