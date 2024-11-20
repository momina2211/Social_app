from django.test import TestCase
from .models import Continent, Country

class GeographyModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name='Asia')
        self.country = Country.objects.create(name='India', continent=self.continent)

    def test_continent_creation(self):
        self.assertEqual(self.continent.name, 'Asia')

    def test_country_creation(self):
        self.assertEqual(self.country.name, 'India')
        self.assertEqual(self.country.continent.name, 'Asia')
