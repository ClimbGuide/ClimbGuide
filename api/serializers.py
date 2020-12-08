from rest_framework import serializers
from climbguide.models import Route, Daytrip, Log
from users.models import User

class NestedLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Log
        fields = [
            "id",
            "username",
            "text",
        ]

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            "id",
            "name",
            "route_type",
            "rating",
            "pitches",
            "location",
            "latitude",
            "longitude",

        ]

class DaytripSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="owners.all", read_only=True)
    logs = NestedLogSerializer(many=True, read_only=True)
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Daytrip
        fields = [
            "id",
            "username",
            "title",
            "description",
            "routes",
            "logs",
        ]