from django.urls import path
from . import views

urlpatterns = [
  path('', views.root, name='root'),
  path('about/', views.about, name='about'),
  path('starwarscards/<int:swc_id>/', views.starwarscards_detail, name='detail'),
  path('starwarscards/', views.StarWarsCardList.as_view(), name='starwarscards_index'),
  path('starwarscards/create/', views.StarWarsCardCreate.as_view(), name='starwarscards_create'),
  path('starwarscards/<int:pk>/update/', views.StarWarsCardUpdate.as_view(), name='starwarscards_update'),
  path('starwarscards/<int:pk>/delete/', views.StarWarsCardDelete.as_view(), name='starwarscards_delete'),
]