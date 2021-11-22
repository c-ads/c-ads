from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

app_name = 'authentication'

urlpatterns = [
    path('user/get/', UserRetrieveUpdateAPIView.as_view()),
    path('user/register/', RegistrationAPIView.as_view()),
    path('user/login/', LoginAPIView.as_view()),
]
