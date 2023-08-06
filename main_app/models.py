from django.db import models
from django.urls import reverse
from django.utils import timezone

class Character(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
      return self.name

    def get_absolute_url(self):
      return reverse('characters_detail', kwargs={'pk': self.id})
  

class StarWarsCard(models.Model):
    SERIES_TYPES = (
      ('B', 'Blue'),
      ('R', 'Red'),
      ('Y', 'Yellow'),
    )
    CONDITION_TYPES = (
      ('Mt', 'Mint'),
      ('Ex', 'Excellent'),
      ('Vg', 'Very Good'),
      ('Gd', 'Good'),
      ('Fr', 'Fair'),
      ('Pr', 'Poor'),
    )
    series_type = models.CharField(max_length=2, choices=SERIES_TYPES)
    card_number = models.IntegerField()
    caption = models.CharField(max_length=100)
    condition_type = models.CharField(max_length=2, choices=CONDITION_TYPES)
    description = models.TextField(max_length=250)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return (f"{self.card_number}: {self.caption}")
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'swc_id': self.id})
    
    def card_is_appreciating(self):
        if self.appraisal_set.all().count() < 2:
          return False
        last_appraisal = self.appraisal_set.all()[0].value
        prev_appraisal = self.appraisal_set.all()[1].value
        return last_appraisal > prev_appraisal
    
    class Meta:
      ordering = ['card_number']
    

class Appraisal(models.Model):
    appr_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100)
    value = models.DecimalField('value ($)', max_digits=8, decimal_places=2)
    starwarscard = models.ForeignKey(StarWarsCard, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.name}: ${self.value}")
    
    class Meta:
      ordering = ['-appr_date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    starwarscard = models.ForeignKey(StarWarsCard, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for starwarscard_id: {self.starwarscard_id} @{self.url}"