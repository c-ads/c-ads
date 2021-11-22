from django.urls import path

from .views import (
    HomeView, user_registration_view, user_login_view, user_page_view
)

app_name = 'saprgramapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration/', user_registration_view, name='registration'),
    path('login/', user_login_view, name='login'),
    path('user/<str:username>/', user_page_view, name='user_page')
]
