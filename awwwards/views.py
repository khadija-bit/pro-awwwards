from django.shortcuts import render,redirect
from .models import Profile, Project, Review,SignUpForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import SignInForm,ProfileForm, ProjectForm,ReviewForm
from django.contrib.auth.models import User
from .email import send_welcome_email
# Create your views here.
def index(request):
    projects = Project.objects.all()
    profile = Profile.objects.all()
    return render(request,'index.html',{"projects":projects,"profile":profile})

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
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    projects = Project.objects.filter(user=current_user)    
    return render(request, 'profile.html',{"profiles":profiles,"projects":projects})

def new_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('profile')
        else:
            form = ProfileForm()

    return render(request, 'new_profile.html',{"form":form})

def signIn(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = SignUpForm(name = name, email=email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('signIn')
    else:
        form = SignInForm()
    return render(request,'registration/registration_form.html',{"form":form})

def project(request,project_id):
    project = Project.objects.get(id = project_id)
    rating = round(((project.design + project.usability + project.content)/3),2)
    if request.method == 'POST':
        form = ReviewForm(request,POST)
        if form.is_valid:
            project.vote_submission += 1
            if project.design == 0:
                project.design = int(request.POST['design'])
            else:
                project.design = int(project.design + int(request.POST['design']))/2
            if project.usability == 0:
                project.usability = int(request.POST['usability'])
            else:
                project.usability = int(project.usability + int(request.POST['usability']))/2
            if project.content == 0:
                project.content = int(request.POST['content'])
            else:
                project.content = int(project.content + int(request.POST['content']))/2        
            project.save()
            return redirect(reverse(project,args=[project_id]))     

    else:
        form = ReviewForm()
    return render(render,'project.html',{"form":form,"project":project,"rating":rating})