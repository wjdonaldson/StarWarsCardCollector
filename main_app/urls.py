from django.urls import path
from . import views

urlpatterns = [
  path('about/', views.about, name='about'),
  path('starwarscards/', views.starwarscards_index, name='index')
]