from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Continent, Country
from .serializers import ContinentSerializer, CountrySerializer

class ContinentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        continents = Continent.objects.all()
        serializer = ContinentSerializer(continents, many=True)
        return Response(serializer.data)


class CountryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        continent_id = request.GET.get('continent')  # Filter by continent if provided
        if continent_id:
            countries = Country.objects.filter(continent_id=continent_id)
        else:
            countries = Country.objects.all()

        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)
