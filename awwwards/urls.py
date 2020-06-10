from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^search/',views.search_results, name='search_results'),
    url(r'^project/(?P<project_id>(\d+)) ',views.rateProject, name='rateProject'),
    url(r'^new_project/',views.submitproject, name='new_project'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^update_profile/',views.updateProfile,name='update_Profile'),
    url(r'^api/project/$', views.ProjectList.as_view(),name='project_api'),
    url(r'^api/profile/$', views.ProfileList.as_view(),name='profile_api'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)