from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    profile_photo = models.ImageField()
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

class Projects(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    description = models.TextField()
    url = models.URLField()
    date = models.DateTimeField()

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
