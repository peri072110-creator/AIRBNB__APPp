from rest_framework import generics, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    PropertyListSerializer,
    PropertyDetailSerializer,
    CitySerializer,
    ReviewSerializer,
    BookingSerializer
)
from .permissions import IsAdmin, IsHost, IsGuest, IsOwnerOrAdmin, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .pagination import PropertyPageNumberPagination
from .filters import PropertyFilterSet

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]



class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_class = PropertyFilterSet
    search_fields = ['title', 'description']
    pagination_class =  PropertyPageNumberPagination
    ordering_fields = ['price_per_night', 'rating', 'created_at']
    ordering = ['price_per_night']


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]


class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    permission_classes = [IsHost | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    permission_classes = [IsOwnerOrAdmin]


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):

        property_id = self.request.query_params.get('property_id')
        if property_id:
            return Review.objects.filter(property__id=property_id)
        return Review.objects.all()


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsGuest]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return Booking.objects.all()
        elif user.role == "HOST":
            return Booking.objects.filter(property__owner=user)
        return Booking.objects.filter(user=user)


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsGuest]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
