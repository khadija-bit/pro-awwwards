from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile, Project, Review,SignUpForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import SignInForm,ProfileForm, ProjectForm,ReviewForm
from django.contrib.auth.models import User
from .email import send_welcome_email
from django.db.models import Avg
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def index(request):
    projects = Project.objects.all()
    profile = Profile.objects.all()
    rating = Review.objects.all()
    form = ReviewForm()
   
    return render(request,'index.html',{"projects":projects,"profile":profile,"rating":rating,"form":form})

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
    profiles = Profile.objects.filter(user=request.user)
    projects = Project.objects.all()
    form = ReviewForm()

    return render(request, 'profile.html',locals())

def updateProfile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        updatProfile = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()

        return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile) 

    return render(request,'update_profile.html',locals())           


def submitproject(request):
    form = ProjectForm()
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        user = request.user.id

        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = current_user
            upload.save()
            return redirect('index')
        else:
            form = ProjectForm()

    return render(request, 'submit_project.html',locals())

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

def rateProject(request, project_id):
    project = get_object_or_404(Project,pk=project_id)
    reviews = Review.objects.filter(projects = project)
    design = reviews.aggregate(Avg('design'))['design__avg']
    usability = reviews.aggregate(Avg('usability'))['usability__avg']
    content = reviews.aggregate(Avg('content'))['content__avg']
    overall_total = reviews.aggregate(Avg('overall_total'))['overall_total__avg']
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.overall_total = (rating.design + rating.usability + rating.content) / 3
            rating.projects = project
            rating.user = request.user
            rating.save()

    return redirect('index')

class ProfileList(APIView):
    def get(self, request,format=None):
        all_merch = Profile.objects.all()
        serializers = ProfileSerializer(all_merch, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectList(APIView):
    def get(self, request,format=None):
        all_merch = Project.objects.all()
        serializers = ProjectSerializer(all_merch, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    