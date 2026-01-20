from .models import UserProfile, Property, Booking, Review, City
from modeltranslation.translator import TranslationOptions,register


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address', 'owner')


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment', )