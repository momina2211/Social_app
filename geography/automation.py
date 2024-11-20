import json
from .models import Continent, Country


def populate_countries_and_continents():
    # Open and read the JSON file
    with open('geography/countries.json') as file:
        data = json.load(file)

        for entry in data:
            continent_name = entry['continent']
            country_name = entry['country']

            # Create or get the continent
            continent, created = Continent.objects.get_or_create(name=continent_name)

            # Create or get the country associated with the continent
            Country.objects.get_or_create(name=country_name, continent=continent)

    print("Data successfully populated!")
