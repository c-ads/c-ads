
from .models import Users
from django.forms import ModelForm, TextInput


class RegForm(ModelForm):
    class Meta:
        model = Users
        fields = ["login", "password", "email"]
        widgets = {
            'login': TextInput(attrs={
                'id': 'username',
                'type': 'text',
                'placeholder': 'Enter login'
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


class LogForm(ModelForm):
    class Meta:
        model = Users
        fields = ["login", "password"]
        widgets = {
            'login': TextInput(attrs={
                'id': 'username',
                'type': 'text',
                'placeholder': 'Enter login'
            }),
            'password': TextInput(attrs={
                'id': 'password',
                'type': 'password',
                'placeholder': 'Enter password'
            })
        }
