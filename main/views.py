from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


#navigation bar views
@login_required
def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def settings(request):
    return render(request, 'settings.html')

#views not on navigation bar
def map(request):
    return render(request, 'map.html')