# Imports
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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
        
class DaytripListCreateView(generics.ListCreateAPIView):
    serializer_class = DaytripSerializer

    def get_queryset(self):
        return self.request.user.daytrips.all()
    
    def perform_create(self, serializer):
        daytrip = serializer.save()
        daytrip.owners.add(self.request.user)
