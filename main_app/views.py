from django.shortcuts import render

starwarscards = [
  {'series': 'Blue',
   'number': 3,
   'caption': 'The little droid, Artoo-Detoo', 
   'condition': 'Fair'
  },
  {'series': 'Blue',
   'number': 5,
   'caption': 'Princess Leia Organa', 
   'condition': 'Poor'
  },
  {'series': 'Red',
   'number': 71,
   'caption': 'The incredible See-Threepio!', 
   'condition': 'Fair'
  },
]

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define the starwarscards view
def starwarscards_index(request):
  return render(request, 'starwarscards/index.html',
                {'starwarscards': starwarscards})
