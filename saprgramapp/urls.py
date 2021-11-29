from django.urls import path

from .views import *

app_name = 'saprgramapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registration/', user_registration_view, name='registration'),
    path('login/', user_login_view, name='login'),
    path('user/<str:username>/', user_page_view, name='user_page'),
    path('user/edit_page', user_edit_page, name='edit_page'),
    path('ourTeam/', our_team_view, name='ourTeam'),
    path('user/addPublication', add_publication_view, name='add_pub'),
    path('tape/', tape_view, name='tape')
]
