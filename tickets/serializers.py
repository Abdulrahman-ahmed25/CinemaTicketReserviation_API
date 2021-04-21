from django.db.models import fields
from rest_framework import serializers
from .models import Movie, Guest, Reservation

#1
class MovieSerialization(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields='__all__'

class GuestSerialization(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields=['pk','reservation','name','mobile']

class ReservationSerialization(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields='__all__'