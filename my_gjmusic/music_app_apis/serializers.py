from rest_framework import serializers
from music_app_apis.models import Person, Destination

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name')