import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import StarWarsCard, Character, Photo
from .forms import AppraisalForm

# if the user goes to the root URL redirect to about
def root(request):
  return redirect('about')

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define the starwarscards view
def starwarscards_index(request):
  starwarscards = StarWarsCard.objects.all()
  return render(request, 'starwarscards/index.html', {'starwarscards': starwarscards})

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

class StarWarsCardList(ListView):
    model = StarWarsCard

    # def get_context_data(self, **kwargs):
    #     appraisal_form = AppraisalForm()
    #     print(appraisal_form)
    #     context = super(StarWarsCardList, self).get_context_data(**kwargs)
    #     context['appraisal_form'] = appraisal_form
    #     return context

class StarWarsCardCreate(CreateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

class StarWarsCardUpdate(UpdateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

class StarWarsCardDelete(DeleteView):
  model = StarWarsCard
  success_url = '/starwarscards'

def add_appraisal(request, swc_id):
  form = AppraisalForm(request.POST)
  if form.is_valid():
    new_appraisal = form.save(commit=False)
    new_appraisal.starwarscard_id = swc_id
    new_appraisal.save()
  return redirect('detail', swc_id=swc_id)

class CharacterList(ListView):
  model = Character

class CharacterDetail(DetailView):
  model = Character

class CharacterCreate(CreateView):
  model = Character
  fields = '__all__'

class CharacterUpdate(UpdateView):
  model = Character
  fields = ['name']

class CharacterDelete(DeleteView):
  model = Character
  success_url = '/characters'

def assoc_character(request, swc_id, character_id):
  StarWarsCard.objects.get(id=swc_id).characters.add(character_id)
  return redirect('detail', swc_id=swc_id)

def unassoc_character(request, swc_id, character_id):
  StarWarsCard.objects.get(id=swc_id).characters.remove(character_id)
  return redirect('detail', swc_id=swc_id)

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