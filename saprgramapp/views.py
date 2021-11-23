from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from .models import Publication, Comments
from .forms import *
import os
import jwt
import requests


def user_registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/user_registration.html', {'form': form})

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        registration_request = {
            'user': {
                'email': email,
                'username': username,
                'password': password,
            }
        }

        try:
            response = requests.post('http://localhost:8000/api/user/register/', json=registration_request)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass # TODO: Handle API errors.

        if 'errors' in response.json():
            pass # TODO: Handle signup errors.
        else:
            return redirect('saprgramapp:login')

    return render(request, 'authentication/user_registration.html', {'form': form})


def user_login_view(request):
    form = LoginForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        login_request = {
             'user': {
                 'email': email,
                 'password': password
             }
         }

        try:
            response = requests.post('http://localhost:8000/api/user/login/', json=login_request)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass # TODO: Handle API errors.

        json = response.json()
        if 'errors' in json:
            context['form'].login_errors = 'Invalid email or password.'
        else:
            response = redirect('/user/{0}/'.format(json['user']['username']))
            response.set_cookie('JWT_TOKEN', json['user']['token'])

            return response

    return render(request, 'authentication/user_login.html', context)


def user_page_view(request, username):
    jwt.decode(request.COOKIES['JWT_TOKEN'][2:-1], settings.SECRET_KEY, algorithms=["HS256"])
    user_data = User.objects.get(username=username)
    user_publications = Publication.objects.filter(user_id=user_data.pk)
    form = ImageLoadForm()
    if request.method == 'POST':

        path = os.path.dirname(__file__)
        path = os.path.dirname(path)

        os.chdir(path + '\\media\\photos\\avatar')
        photo = request.FILES['avatar_photo']
        user_data = get_object_or_404(User, username=username)
        form = ImageLoadForm(data=request.POST, files=request.FILES, instance=user_data)

        if form.is_valid():

            if not os.path.exists(str(photo)):
                form.save(commit=True)
    user_data = User.objects.get(username=username)
    context = {
        'user_data': user_data,
        'number_of_posts': len(user_publications),
        'user_posts': user_publications,
        'form': form
    }
    return render(request, 'userpage/user_page.html', context)


class HomeView(TemplateView):
    template_name = 'home/index.html'
