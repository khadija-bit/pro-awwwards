from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^search/',views.search_results, name='search_results'),
    url(r'^profile/<int:project_id>',views.profile, name='profile'),
    url(r'^new_project/',views.submitproject, name='new_project'),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)