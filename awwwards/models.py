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