from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from user import views
from user.views import *

app_name = 'user'

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
    path('recipe/', views.userrecipe, name='recipeprofile'),
    path('youtube/', views.useryoutube, name='youtubeprofile'),
    path('hotplace/', views.userhotplace, name='hotplaceprofile'),
    path('user/<int:pk>', PostUserProfile.as_view(), name = 'userprofile'),
    path('recipe/<int:pk>', PostUserRecipe.as_view(), name = 'userrecipe'),
    path('youtube/<int:pk>', PostUserYoutube.as_view(), name='useryoutube'),
    path('hotplace/<int:pk>', PostUserHotplace.as_view(), name='userhotplace'),
]