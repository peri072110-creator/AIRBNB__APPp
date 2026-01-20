from django_filters import FilterSet
from .models import Property, City
class PropertyFilterSet(FilterSet):
    class Meta:
        model = Property
        fields = {
            'city': ['exact'],
            'property_type': ['exact'],
            'max_guests': ['gte'],
            'price_per_night': ['gte', 'lte'],

        }


class CityFilterSet(FilterSet):

    class Meta:
        model = City
        fields = ['name']