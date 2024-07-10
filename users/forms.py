from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': TextInput(attrs={
                'class': "border-gray-300 border-2 rounded-lg w-full py-4 bg-slate-100 text-gray-600 focus:outline-none focus:shadow-outline",
                'placeholder': 'Username'
                }),
            'email': EmailInput(attrs={
                'class': "border-gray-300 border-2 rounded-lg w-full py-4 bg-slate-100 text-gray-600 focus:outline-none focus:shadow-outline",
                'placeholder': 'Email'
                })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            'class': "border-gray-300 border-2 rounded-lg w-full py-4 bg-slate-100 text-gray-600 focus:outline-none focus:shadow-outline",
            'placeholder': 'Password'
        })
        self.fields["password2"].widget.attrs.update({
            'class': "border-gray-300 border-2 rounded-lg w-full py-4 bg-slate-100 text-gray-600 focus:outline-none focus:shadow-outline",
            'placeholder': 'Confirm Password'
        })
