from django.urls import path
from .views import ContinentListView, CountryListView

urlpatterns = [
    path('continents/', ContinentListView.as_view(), name='continent_list'),
    path('countries/', CountryListView.as_view(), name='country_list'),
]
