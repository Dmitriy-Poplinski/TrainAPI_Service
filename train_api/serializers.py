from django.contrib.auth.models import User
from rest_framework import serializers

from train_api.models import Crew, Station, TrainType, Train, Route, Journey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class StationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("name",)


class StationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainListSerializer(serializers.ModelSerializer):
    train_type = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = TrainType
        fields = ("name", "train_type")


class TrainDetailSerializer(serializers.ModelSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type",)


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Route
        fields = ("distance", "source", "destination",)


class RouteDetailSerializer(serializers.ModelSerializer):
    source = StationDetailSerializer()
    destination = StationDetailSerializer()

    class Meta:
        model = Route
        fields = "__all__"


class JourneyListSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(read_only=True, slug_field="full_route")
    train = serializers.SlugRelatedField(read_only=True, slug_field="name")
    crews = serializers.SlugRelatedField(read_only=True, slug_field="full_name", many=True)

    class Meta:
        model = Journey
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews",)


class JourneyDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailSerializer()
    train = TrainDetailSerializer()
    crews = CrewSerializer(many=True)

    class Meta:
        model = Journey
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews",)