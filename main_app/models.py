from django.db import models
from django.urls import reverse

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

    def __str__(self):
        return (f"{self.card_number}: {self.caption}")
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'swc_id': self.id})