from rest_framework import serializers
from .models import Continent, Country

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    continent = ContinentSerializer()  # Include continent details in the response

    class Meta:
        model = Country
        fields = ['id', 'name', 'continent']
