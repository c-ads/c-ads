from django.forms import ModelForm, TextInput, FileInput

from authentication.models import User


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': TextInput(attrs={
                'id': 'username',
                'type': 'username',
                'placeholder': 'Enter username'
            }),
            'password': TextInput(attrs={
                'id': 'password',
                'type': 'password',
                'placeholder': 'Enter password'
            }),
            'email': TextInput(attrs={
                'id': 'email',
                'type': 'email',
                'placeholder': 'Enter email'
            })
        }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': TextInput(attrs={
                'id': 'email',
                'type': 'email',
                'placeholder': 'Enter email'
            }),
            'password': TextInput(attrs={
                'id': 'password',
                'type': 'password',
                'placeholder': 'Enter password'
            })
        }


class ImageLoadForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar_photo']
        widgets = {
            'avatar_photo': FileInput(attrs={
                'id': 'avatar',
                'type': 'file',
                'placeholder': 'Upload photo'
            })
        }
