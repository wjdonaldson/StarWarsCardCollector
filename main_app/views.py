from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import StarWarsCard

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
  return render(request, 'starwarscards/detail.html', {'starwarscard': starwarscard})

class StarWarsCardList(ListView):
    model = StarWarsCard

class StarWarsCardCreate(CreateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

class StarWarsCardUpdate(UpdateView):
  model = StarWarsCard
  fields = ['series_type', 'card_number', 'caption', 'condition_type', 'description']

class StarWarsCardDelete(DeleteView):
  model = StarWarsCard
  success_url = '/starwarscards'
