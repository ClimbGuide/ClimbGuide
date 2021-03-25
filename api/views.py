# Imports
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import json
# Local File Imports
from .serializers import RouteSerializer, DaytripSerializer
from climbguide.models import Route, Daytrip, Log

# Views

# Route Views
class RouteListView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.all()


class RouteSearchView(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["route_type", "rating"]


# Daytrip Views
class DaytripListCreateView(generics.ListCreateAPIView):
    serializer_class = DaytripSerializer

    def get_queryset(self):
        return self.request.user.daytrips.all()
    
    def perform_create(self, serializer):
        daytrip = serializer.save()
        daytrip.owners.add(self.request.user)

class UpdateDaytripRoutesView(APIView):
    def post(self, request, daytrip_pk):
        daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
        daytrip.routes.clear()
        routes = json.loads(request.body)
        for route in routes["routes"]:
            route_obj = Route.objects.get(
                pk=route["route_pk"]
            )
            daytrip.routes.add(route_obj)
        serializer = DaytripSerializer(instance=daytrip)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Log Views
class LogCreateView(APIView):
    def post(self, request, daytrip_pk):
        daytrip = get_object_or_404(request.user.daytrips, pk=daytrip_pk)
        serializer = DaytripSerializer(instance=daytrip)
        if request.user in daytrip.owners.all():
            json_log = json.loads(request.body)
            log_text = json_log["log"]
            Log.objects.create(
                text=log_text,
                owner=request.user,
                daytrip=daytrip
            )
            if serializer.is_valid:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        

