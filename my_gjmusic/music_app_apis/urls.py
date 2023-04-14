# Whenever we create a app, we always neeed to create a urls.py file

from django.contrib import admin
from django.urls import path
from . import views
from django.urls import re_path as url

###local:8000/studyplanner/index
urlpatterns = [
    # path('person', views.person_details),
    # path('product_details_es', views.product_details_es)
    path('upload_song', views.upload_songs),
    path('get_all_songs', views.get_all_songs),
    path('login', views.login_user),
    path('playlist', views.update_playlist),
    path('recommend_to_friend', views.recommend_song_to_friend),
    path('suggest_by_search', views.suggest_by_search),
    path('recommended_for_you', views.recommended_for_you)
]