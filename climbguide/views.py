# Django Imports
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector


# Project Files Imports 
from .models import Route

# Create your views here.
def home(request):
    routes = Route.objects.all()
    mapbox_access_token = 'pk.eyJ1IjoiYmVsb25nYXJvYmVydCIsImEiOiJja2c2cWd2N3IwdGluMnBwaWV5ZzU2bjhnIn0.QgRdSLNmSGfcu1CMWF7vhw'
    return render(request, "home.html", {
        'mapbox_access_token': mapbox_access_token,
        "routes": routes
    })

def search(request):
    query = request.GET.get('q', '')
    if query is not None:
        routes = Route.objects.annotate(
            search=SearchVector("name", "location")
        ).filter(search=query)
    else:
        routes = None
    return render(request, 'climbguide/search.html', {
        "routes": routes,
        "query": query or ""
    })

def route_detail(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    if route.pitches == '':
        pitches = False
    else:
        pitches = True
    return render(request, "climbguide/route_detail.html", {
        "route": route,
        "pitches": pitches
    })
