from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from .models import  *
from django.utils.translation import get_language
from .models import Property, City
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ( 'first_name',   'username','email', 'password',  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'phone_number','email', 'first_name', 'last_name', 'avatar')
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('image',)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ( 'property','guest','rating', 'id', 'rating', 'comment' )

class PropertyDetailSerializer(serializers.ModelSerializer):
     images = PropertyImageSerializer(many=True, read_only=True)
     reviews = ReviewSerializer(many=True, read_only=True)
     owner = UserProfileSerializer(read_only=True)
     class Meta:
        model = Property
        fields =   ['id', 'title', 'description', 'price_per_night', 'address',
                    'max_guests' ,'rules','property_type', 'city', 'images',
                    'bedrooms', 'bathrooms', 'owner', 'reviews']

        def get_avg_rating(self, obj):
            return obj.get_avg_rating()

        def get_count_people(self, obj):
            return obj.get_count_people()
class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', ]

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'title', 'description', 'price_per_night', 'address', 'property_type', 'city')


class PropertyListSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    images = PropertyImageSerializer(many=True )

    class Meta:
        model = Property
        fields = ('id', 'title', 'description', 'price_per_night', 'address', 'property_type', 'city', 'images')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields =  '__all__'
        extra_kwargs = {'booking_status': {'read_only': True}}







