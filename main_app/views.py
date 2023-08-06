import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StarWarsCard, Character, Photo
from .forms import AppraisalForm

# if the user goes to the root URL redirect to about
def root(request):
  return redirect('about')

def about(request):
  return render(request, 'about.html')

# @login_required
# def starwarscards_index(request):
#   starwarscards = StarWarsCard.objects.filter(user=request.user)
#   return render(request, 'starwarscards/index.html', {'starwarscards': starwarscards})

@login_required
def starwarscards_detail(request, swc_id):
  starwarscard = StarWarsCard.objects.get(id=swc_id)
  id_list = starwarscard.characters.all().values_list('id')
  characters_starwarscard_doesnt_have = Character.objects.exclude(id__in=id_list)
  appraisal_form = AppraisalForm()
  return render(request, 'starwarscards/detail.html', 
                {'starwarscard': starwarscard,
                 'appraisal_form': appraisal_form,
                 'characters': characters_starwarscard_doesnt_have
                 })

class StarWarsCardList(LoginRequiredMixin, ListView):
    model = StarWarsCard

    def get_queryset(self):
      return StarWarsCard.objects.filter(user=self.request.user)

class StarWarsCardCreate(LoginRequiredMixin, CreateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class StarWarsCardUpdate(LoginRequiredMixin, UpdateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

class StarWarsCardDelete(LoginRequiredMixin, DeleteView):
  model = StarWarsCard
  success_url = '/starwarscards'

@login_required
def add_appraisal(request, swc_id):
  form = AppraisalForm(request.POST)
  if form.is_valid():
    new_appraisal = form.save(commit=False)
    new_appraisal.starwarscard_id = swc_id
    new_appraisal.save()
  return redirect('detail', swc_id=swc_id)

class CharacterList(LoginRequiredMixin, ListView):
  model = Character

class CharacterDetail(LoginRequiredMixin, DetailView):
  model = Character

class CharacterCreate(LoginRequiredMixin, CreateView):
  model = Character
  fields = '__all__'

class CharacterUpdate(LoginRequiredMixin, UpdateView):
  model = Character
  fields = ['name']

class CharacterDelete(LoginRequiredMixin, DeleteView):
  model = Character
  success_url = '/characters'

@login_required
def assoc_character(request, swc_id, character_id):
  StarWarsCard.objects.get(id=swc_id).characters.add(character_id)
  return redirect('detail', swc_id=swc_id)

@login_required
def unassoc_character(request, swc_id, character_id):
  StarWarsCard.objects.get(id=swc_id).characters.remove(character_id)
  return redirect('detail', swc_id=swc_id)

@login_required
def add_photo(request, swc_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, starwarscard_id=swc_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', swc_id=swc_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('starwarscards_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
