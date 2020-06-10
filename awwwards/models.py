from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=300,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.user.username}'

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)    
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.save() 

class Project(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, default='')
    description = models.TextField()
    url = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.title}'

    def save_projects(self):
        self.save()

    def delete_projects(self):
        self.delete()

    @classmethod
    def search_projects(cls,search_term):
        title = cls.objects.filter(title__icontains = search_term)
        return title  

    @classmethod
    def all_project(cls):
        return cls.objects.all()    


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    design = models.IntegerField(choices=RATING_CHOICES)
    usability = models.IntegerField(choices=RATING_CHOICES)
    content = models.IntegerField(choices=RATING_CHOICES)
    overall_total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    projects = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.design}'

    @classmethod
    def all_reviews(cls, id):
        reviews = Review.objects.filter(project_id = id).all()
        return reviews

class SignUpForm(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()