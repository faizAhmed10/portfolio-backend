from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path("website/", getWebsiteCard, name="webcard"),
    path("website/<str:pk>", getWebsite, name="webInfo"),
    path("testimonials/", getTestimonials, name="testimonials"),
    path("create-testimonial/", createTestimonial, name = "create-testimonial"),
    path('register/', registerUser, name='user-registration'),
    path('contact/', postForm, name="post-form"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
