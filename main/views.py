from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegForm, LogForm
from .models import Users, Posts, Comments
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.


def index(request):
    data = Users.objects.all()
    return render(request, "main/index.html", {'data': data})


def sign_in(request):
    logins = list(Users.objects.values_list('login', flat=True))
    passwords = list(Users.objects.values_list('password', flat=True))

    form = LogForm()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        user_login = request.POST.get('login')  # приймає дані рядка логін з форми
        user_password = request.POST.get('password')  # приймає дані рядка password з форми

        for login in logins:
            if login == user_login and check_password(user_password, passwords[logins.index(user_login)]):
                return redirect(f'user/{login}/')

        context['form'].invalid_password_or_login = 'Invalid password or login, try again.'

    return render(request, 'main/sign_in.html', context)


def sign_up(request):
    logins = list(Users.objects.values_list('login', flat=True))
    emails = list(Users.objects.values_list('email', flat=True))

    form = RegForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = RegForm(request.POST)

        login = form.data['login']  # отримуємо дані з форми
        email = form.data['email']
        password = make_password(form.data['password'])
        if form.is_valid() and login not in logins and email not in emails:
            Users.objects.create(login=login, email=email, password=password)

            return redirect('home')
        else:
            context['form'].user_is_already_registered = 'User with this email or login is already registered.'

    return render(request, 'main/sign_up.html', context)


def user(request, user_login):
    data = Users.objects.filter(login=user_login)

    user_id = None
    for i in data:
        user_id = i.id
    post = Posts.objects.filter(user_id_id=user_id)
    return render(request, 'main/user.html', {'data': data, 'post': post})


def post(request, user_login, post_id):
    post = Posts.objects.filter(id=post_id)
    comments = Comments.objects.filter(post_id_id=post_id)
    print(comments)
    return render(request, 'main/post.html', {'post': post, 'comments': comments})
