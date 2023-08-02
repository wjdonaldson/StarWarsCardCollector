from django.urls import path
from . import views

urlpatterns = [
  path('', views.root, name='root'),
  path('about/', views.about, name='about'),
  path('starwarscards/', views.starwarscards_index, name='index'),
  path('starwarscards/<int:swc_id>/', views.starwarscards_detail, name='detail'),
]