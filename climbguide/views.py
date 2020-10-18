# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector

# Project Files Imports 
from .models import Route, Daytrip
from .forms import DaytripForm, PhotoForm

# Views
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
    photos = route.photos.all()
    if route.pitches == '':
        pitches = False
    else:
        pitches = True
    return render(request, "climbguide/route_detail.html", {
        "route": route,
        "photos": photos,
        "pitches": pitches,
        "PhotoForm": PhotoForm
    })


@login_required
def add_daytrip(request):
    if request.method == "GET":
        form = DaytripForm()
    else:
        form = DaytripForm(request.POST)
        if form.is_valid:
            daytrip = form.save()
            daytrip.owners.add(request.user)
            daytrip.save()
            return redirect("daytrip_detail", daytrip_pk=daytrip.pk)
        return render(request, "climbguide/add_daytrip.html", {
            "form": form
        })


@login_required
def daytrip_detail(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    routes = Route.objects.all()
    planned_routes = daytrip.routes.all()
    owners = daytrip.owners.all()
    mapbox_access_token = 'pk.eyJ1IjoiYmVsb25nYXJvYmVydCIsImEiOiJja2c2cWd2N3IwdGluMnBwaWV5ZzU2bjhnIn0.QgRdSLNmSGfcu1CMWF7vhw'
    return render(request, "climbguide/daytrip_detail.html", {
        "daytrip": daytrip,
        "routes": routes,
        "planned_routes": planned_routes,
        "owners": owners,
        "mapbox_access_token": mapbox_access_token,
        "DaytripForm": DaytripForm
    })


@login_required
def delete_daytrip(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    if request.method == "POST":
        daytrip.routes.clear()
        daytrip.users.clear()
        daytrip.delete()
        return redirect("home")
    return render(request, "climbguide/delete_daytrip.html", {
        "daytrip": daytrip
    })


@login_required
def edit_daytrip(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    if request.method == "GET":
        form = DaytripForm(instance=daytrip)
    else:
        form = DaytripForm(request.POST, instance=daytrip)
        if form.is_valid:
            form.save()
            return redirect("daytrip_detail", daytrip_pk=daytrip.pk)
    return render(request, "climbguide/edit_daytrip.html", {
        "daytrip": daytrip,
        "form": form
    })


@login_required
def addphoto_to_route(request, route_pk):
    if request.method == "GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        route = get_object_or_404(Route, pk=route_pk)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.route = route
            photo.save()
            return redirect("route_detail", route_pk=route.pk)
    return render(request, "climbguide/addphoto_to_route.html", {
        "form": form
    })