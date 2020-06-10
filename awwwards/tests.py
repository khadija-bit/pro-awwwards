from django.test import TestCase
from .models import Profile,Project,Review

# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.khadija = Profile(profile_photo='khadija')
        self.khadija.save()
    
    def test_instance(self):
        self.assertTrue(isinstance(self.khadija, Profile))

    def test_save_method(self):
        self.khadija.save_profile()
        khadija = Profile.objects.all()
        self.assertTrue(len(editors) > 0)   


class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project(title='khadija',image='',url='')
        

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project)) 
    
    def test_save_method(self):
        self.khadija.save_projects()
        project = Project.objects.all()
        self.assertTrue(len(editors) > 0)
       

class ReviewTest(TestCase):
    def setUp(self):
        self.rating = Review(design='khadija')

    def test_instance(self):
        self.assertTrue(isinstance(self.rating,Review))  

    def test_save_method(self):
        self.khadija.all_reviews()
        rating = Review.objects.all()
        self.assertTrue(len(editors) > 0) 
                  