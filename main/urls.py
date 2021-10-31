from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='home'),
    path('sign_up', sign_up, name='sign_up'),
    path('sign_in', sign_in, name='sign_in'),
    path('user/<str:user_login>/', user),
    path('user/<str:user_login>/<int:post_id>/', post)
]