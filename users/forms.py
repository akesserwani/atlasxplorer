from django import forms
from django.forms import TextInput, EmailInput, PasswordInput, ModelForm
from django.contrib.auth.models import User
from main.models import UserMap, Pin
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

#forms for creating new 
class CreateMap(forms.Form):
    name = forms.CharField(max_length=30, min_length=1)
    private = forms.BooleanField(required=False)


class UpdateMap(ModelForm):
    name = forms.CharField(max_length=30, min_length=1)

    class Meta:
        model = UserMap
        fields = ['name',]  

class CreatePin(forms.Form):
    name = forms.CharField(max_length=30, min_length=1)
    lat = forms.IntegerField()
    long = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea, max_length=1500, required=False) 
