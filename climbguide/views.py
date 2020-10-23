# Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
import environ

# Project Files Imports 
from .models import Route, Daytrip, Pointofinterest
from .forms import DaytripForm, PhotoForm, PointofinterestForm, LocationForm

# Set env()
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),)
environ.Env.read_env()


# Views
def home(request):
    route_info = []
    mapbox_access_token = env('MAPBOX_KEY')
    location_q = request.GET.get("location","")
    route_type_q = request.GET.get("route_type","")
    rating_q = request.GET.get("rating", "")
    
    if location_q is not None:
        routes = Route.objects.annotate(
            search=SearchVector("location", "route_type", "rating")
        ).filter(search=location_q).filter(search=route_type_q).filter(search=rating_q)
    else:
        routes = None

    if routes is not None:
        for route in routes:
            route_info.append({
                "name": route.name,
                "pk": route.pk,
                "longitude": route.longitude,
                "latitude": route.latitude,
                "route_type": route.route_type,
                "rating": route.rating,
            })

    return render(request, "home.html", {
        'mapbox_access_token': mapbox_access_token,
        "route_info": route_info,
        "SearchQueryForm": SearchQueryForm,
        "routes": routes,
        "location_q": location_q or "",
        "route_type_q": route_type_q or "",
        "rating_q": rating_q or ""
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


# Route
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


# Daytrip
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
            return redirect("edit_daytrip", daytrip_pk=daytrip.pk)
        return render(request, "climbguide/add_daytrip.html", {
            "form": form
        })


@login_required
def daytrip_detail(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    route_info = []
    routes = daytrip.routes.all()
    owners = daytrip.owners.all()
    pointsofinterest = daytrip.points_of_interest.all()
    mapbox_access_token = env("MAPBOX_KEY")
    for route in routes:
        route_info.append({
            "name": route.name,
            "pk": route.pk,
            "longitude": route.longitude,
            "latitude": route.latitude,
            "route_type": route.route_type,
            "rating": route.rating,
        })
    return render(request, "climbguide/daytrip_detail.html", {
        "daytrip": daytrip,
        "owners": owners,
        "routes": routes,
        "route_info": route_info,
        "mapbox_access_token": mapbox_access_token
    })


@login_required
def delete_daytrip(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    if request.method == "POST":
        daytrip.routes.clear()
        daytrip.points_of_interest.clear()
        daytrip.owners.clear()
        daytrip.delete()
        return redirect("home")
    return render(request, "climbguide/delete_daytrip.html", {
        "daytrip": daytrip
    })


@login_required
def edit_daytrip(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    mapbox_access_token = env("MAPBOX_KEY")
    routes = Route.objects.all()[:20]
    planned_routes = daytrip.routes.all()
    pointsofinterest = Pointofinterest.objects.all()
    planned_pointofinterest = daytrip.points_of_interest.all()
    route_info = []
    location_q = request.GET.get("location","")
    route_type_q = request.GET.get("route_type","")
    rating_q = request.GET.get("rating", "")
    
    if location_q is not None:
        routes = Route.objects.annotate(
            search=SearchVector("location", "route_type", "rating")
        ).filter(search=location_q).filter(search=route_type_q).filter(search=rating_q)
    else:
        routes = None

    if routes is not None:
        for route in routes:
            route_info.append({
                "name": route.name,
                "pk": route.pk,
                "longitude": route.longitude,
                "latitude": route.latitude,
                "route_type": route.route_type,
                "rating": route.rating,
            })

    if request.method == "GET":
        form = DaytripForm(instance=daytrip)
    else:
        form = DaytripForm(request.POST, instance=daytrip)
        if form.is_valid:
            form.save()
            return redirect("daytrip_detail", daytrip_pk=daytrip.pk)
    return render(request, "climbguide/edit_daytrip.html", {
        "daytrip": daytrip,
        "form": form,
        "routes": routes,
        "planned_routes": planned_routes,
        "pointsofinterest": pointsofinterest,
        "planned_pointofinterest": planned_pointofinterest,
        "route_info": route_info,
        "mapbox_access_token": mapbox_access_token
    })


@login_required
@csrf_exempt
@require_POST
def addroutes_to_daytrip(request, daytrip_pk):
    daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
    if request.method == "POST":
        routes = json.loads(request.body)
        daytrip.routes.clear()
        print(daytrip.routes.all())
        for route in routes["routes"]:
            route_obj = Route.objects.get(
                pk=route["route_pk"]
            )
            daytrip.routes.add(route_obj)
        print(daytrip.routes.all())
    return JsonResponse({"RoutesAdded": True})




# Point of Interest
@login_required
def add_pointofinterest(request):
    if request.method == "GET":
        form = PointofinterestForm()
    else:
        form = PointofinterestForm(request.POST, files=request.FILES)
        if form.is_valid:
            pointofinterest = form.save(commit=False)
            pointofinterest.owner = request.user
            pointofinterest.save()
            return redirect("pointofinterest_detail", pointofinterest_pk=pointofinterest.pk)
    return render(request, "climbguide/add_pointofinterest.html", {
        "form": form
    })


def pointofinterest_detail(request, pointofinterest_pk):
    pointofinterest = get_object_or_404(Pointofinterest, pk=pointofinterest_pk)
    photos = pointofinterest.photos.all()
    return render(request, "climbguide/pointofinterest_detail.html", {
        "pointofinterest": pointofinterest,
        "photos": photos,
        "PointofinterestForm": PointofinterestForm(instance=pointofinterest),
        "PhotoForm": PhotoForm
    })


@login_required
def edit_pointofinterest(request, pointofinterest_pk):
    pointofinterest = get_object_or_404(Pointofinterest, pk=pointofinterest_pk)
    if request.method == "GET":
        form = PointofinterestForm(instance=pointofinterest)
    else:
        form = PointofinterestForm(request.POST, instance=pointofinterest)
        if form.is_valid:
            form.save()
            return redirect("pointofinterest_detail", pointofinterest_pk=pointofinterest.pk)
    return render(request, "climbguide/edit_pointofinterest.html", {
        "pointofinterest": pointofinterest,
        "form": form
    })


@login_required
def delete_pointofinterest(request, pointofinterest_pk):
    pointofinterest = get_object_or_404(Pointofinterest, pk=pointofinterest_pk)
    if request.method == "POST":
        pointofinterest.delete()
        return redirect("home")
    return render(request, "climbguide/delete_pointofinterest.html", {
        "pointofinterest": pointofinterest
    })


@login_required
def addphoto_to_pointofinterest(request, pointofinterest_pk):
    if request.method == "GET":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, files=request.FILES)
        pointofinterest = get_object_or_404(Pointofinterest, pk=pointofinterest_pk)
        if form.is_valid:
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.point_of_interest = pointofinterest
            photo.save()
            return redirect("pointofinterest_detail", pointofinterest_pk=pointofinterest.pk)
    return render(request, "climbguide/addphoto_to_pointofinterest.html", {
        "form": form
    })

@login_required
def addlocation_to_pointofinterest(request, pointofinterest_pk):
    if request.method == "GET":
        form = LocationForm()
    else:
        form = LocationForm(request.POST)
        point_of_interest = get_object_or_404(Pointofinterest, pk=pointofinterest_pk)
        if form.is_valid:
            location = form.save()
            point_of_interest.location = location
            point_of_interest.save()
            return redirect("pointofinterest_detail", pointofinterest_pk=point_of_interest.pk)
    return render(request, "climbguide/add_poi_location.html", {
        "form": form
    })