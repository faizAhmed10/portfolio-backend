from rest_framework.serializers import ModelSerializer
from rest_framework import serializers 
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class WebsiteSerializer(ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'
        
class TestimonialsSerializer(ModelSerializer):
    class Meta:
        model = Testimonials
        fields = '__all__'
        
class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'], 
            password=validated_data['password']
        )
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


        
