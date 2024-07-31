from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
# Django Import 
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.conf import settings

# Rest Framework Import
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.serializers import Serializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
# Rest Framework JWT 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.db.models import Case, When, Value, CharField, Q
# Local Import 
from api.models import *

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/website/',
        '/api/website/<str:pk>/',
        '/api/testimonials/',
        '/api/create-testimonial/',
        '/api/token/',
        '/api/token/refresh',
        '/api/register',
        '/api/contact'
]
    return Response(routes)

@api_view(['GET'])
def getWebsiteCard(request):
    # Define a case statement to order by whether ReactJS and Django are present
    siteInfo = Website.objects.annotate(
        has_react_django=Case(
            When(Q(built_with__icontains='ReactJS') & Q(built_with__icontains='Django'), then=Value(1)),
            default=Value(0),
            output_field=CharField()
        )
    )

    # Order by the case statement and any other criteria you may have
    siteInfo = siteInfo.order_by('-has_react_django', '-built_with')

    serializer = WebsiteSerializer(siteInfo, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTestimonials(request):
    testimonials = Testimonials.objects.all()
    serializer = TestimonialsSerializer(testimonials, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getWebsite(request, pk): 
    siteInfo = Website.objects.get(id = pk)
    serializer = WebsiteSerializer(siteInfo, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def postForm(request):
    data = request.data
    
    name = data['name']
    email = data['email']
    message = data['message']
    
    try:
        send_mail(
            'Contact Form',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            settings.EMAIL_HOST_USER,
            ['faizahmed10604@gmail.com'],
            fail_silently=False
        )
        return Response({'success': True})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTestimonial(request):
    user = request.user
    data = request.data
    
    testimonial = Testimonials.objects.create(
            user = user, 
            name = data['name'],
            comment = data['comment']
    )
    
    testimonial.save()
    return Response("Testimonial uploaded. Thanks for your feedback")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        # Check if user already exists
        if User.objects.filter(email=data['email']).exists():
            raise Exception("User already exists")

        # Create the user
        user = User.objects.create(
            username=data['email'], 
            email=data['email'],
            password=make_password(data['password']),
        )

        # Save the user
        user.save()

        # Serialize and return response
        serializer = UserRegistrationSerializer(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message = {'details': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

