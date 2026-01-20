from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserListAPIView,
    CityListAPIView,
    CityDetailAPIView,
    PropertyListAPIView,
    PropertyDetailAPIView,
    PropertyCreateAPIView,
    PropertyUpdateDeleteAPIView,
    ReviewListAPIView,
    ReviewCreateAPIView,
    BookingListAPIView,
    BookingCreateAPIView,
)
router = DefaultRouter()

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListAPIView.as_view(), name='user-list'),

    path('cities/', CityListAPIView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailAPIView.as_view(), name='city-detail'),

    path('properties/', PropertyListAPIView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property-detail'),


    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review-create'),

    path('bookings/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),
]
