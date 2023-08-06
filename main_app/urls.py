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
  path('starwarscards/<int:swc_id>/add_appraisal/', views.add_appraisal, name='add_appraisal'),
  path('starwarscards/<int:swc_id>/add_photo/', views.add_photo, name='add_photo'),
  path('starwarscards/<int:swc_id>/assoc_character/<int:character_id>/', views.assoc_character, name='assoc_character'),
  path('starwarscards/<int:swc_id>/unassoc_character/<int:character_id>/', views.unassoc_character, name='unassoc_character'),
  path('characters/', views.CharacterList.as_view(), name='characters_index'),
  path('characters/<int:pk>/', views.CharacterDetail.as_view(), name='characters_detail'),
  path('characters/create/', views.CharacterCreate.as_view(), name='characters_create'),
  path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='characters_update'),
  path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='characters_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]