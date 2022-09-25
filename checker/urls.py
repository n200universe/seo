
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('projects', views.ListCreateProjectsView.as_view()),
    path('projects/<int:pk>', views.UpdateDeleteProjectsView.as_view()),
    path('keywords', views.ListCreateKeywordsCheckerView.as_view()),
    path('keywords/<int:pk>', views.DetailKeywordView.as_view()),
    path('keywords/p/<int:projectId>', views.KeywordsList.as_view()),
    path('update/<int:pk>', views.UpdateKeywordByProject.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)