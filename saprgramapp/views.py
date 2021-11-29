from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from .models import Publication, Comments
from saprgram.settings import BASE_DIR
from .forms import *
import os
import jwt
import requests


class HomeView(TemplateView):
    template_name = 'home/index.html'


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
            os.chdir(str(BASE_DIR) + f'\\media\\photos\\publications')
            user_dir = f'user_{User.objects.get(email=email).id}'
            if not os.path.exists(user_dir):
                os.mkdir(user_dir)
            return response

    return render(request, 'authentication/user_login.html', context)


def user_page_view(request, username):
    public = jwt.decode(request.COOKIES['JWT_TOKEN'][2:-1], settings.SECRET_KEY, algorithms=["HS256"])
    user_data = User.objects.get(username=username)
    user_publications = Publication.objects.filter(user_id=user_data.pk)

    user_data = User.objects.get(username=username)
    if public['id'] == user_data.id:
        context = {
            'user_data': user_data,
            'user_posts': user_publications,
            'logged': 1
        }

    else:
        context = {
            'user_data': user_data,
            'user_posts': user_publications,
            'logged': 0
        }
    print(context['logged'])
    return render(request, 'userpage/user_page.html', context)


@csrf_protect
def add_publication_view(request):
    user_id = jwt.decode(request.COOKIES['JWT_TOKEN'][2:-1], settings.SECRET_KEY, algorithms=["HS256"])['id']
    form = AddingPublicationForm()
    if request.method == 'POST':
        form = AddingPublicationForm(request.POST, request.FILES)

        os.chdir(str(BASE_DIR) + f'\\media\\photos\\publications\\user_{user_id}')

        if form.is_valid() and not os.path.exists(str(request.FILES['user_photo'])):
            new_pub = form.save(commit=False)
            new_pub.user_id = user_id
            new_pub.save()
    context = {'form': form}
    return render(request, 'userpage/Adding_Publications.html', context)


def tape_view(request):
    posts = Publication.objects.all()[::-1]

    context = {
        'posts': posts
    }
    return render(request, 'tape/tape.html', context)


def user_edit_page(request):
    public = jwt.decode(request.COOKIES['JWT_TOKEN'][2:-1], settings.SECRET_KEY, algorithms=["HS256"])
    user_data = User.objects.get(pk=public['id'])
    form = UserEditForm()
    if request.method == 'POST':

        os.chdir(str(BASE_DIR) + '\\media\\photos\\avatar')

        user_data = get_object_or_404(User, id=public['id'])
        form = UserEditForm(data=request.POST, files=request.FILES, instance=user_data)

        if form.is_valid():
            if request.FILES:
                photo = request.FILES['avatar_photo']
                if not os.path.exists(str(photo)):
                    form.save(commit=True)
            else:

                form.save(commit=True)
    context = {
       'user_data': user_data,
        'form': form
    }
    return render(request, 'userpage/Editting_page.html', context)


def our_team_view(request):
    return render(request, 'home/ourTeam.html')