from django.contrib import admin
from django.urls import path
from recipe.views import *
from . import views


app_name = 'recipe'


urlpatterns = [
    path('', RecipeLV.as_view(), name='recipe_listview'),
    path('post/', RecipeLV.as_view(), name='recipe_listview'),
    path('<int:pk>', RecipeDV.as_view(), name='recipe_detail'),
    path('youtube/<int:pk>', YoutubeDV.as_view(), name='youtube_detail'),
    path('add_recipe/', RecipeCreateView.as_view(), name='recipe_create'),
    path('add_youtube/', YoutubeCreateView.as_view(), name='youtube_create'),
    path('recipe_update/<int:pk>/', RecipeUpdateView.as_view(), name="recipe_update"),
    path('youtube_update/<int:pk>/', YoutubeUpdateView.as_view(), name="youtube_update"),
    path('recipe_delete/<int:pk>/', RecipeDeleteView.as_view(), name="recipe_delete"),
    path('youtube_delete/<int:pk>/', YoutubeDeleteView.as_view(), name="youtube_delete"),
    path('recipe_like/', views.recipe_like, name='recipe_like'),
    path('youtube_like/', views.youtube_like, name='youtube_like'),

]