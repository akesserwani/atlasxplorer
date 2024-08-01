from django import forms
from django.forms import TextInput, EmailInput, PasswordInput, ModelForm
from django.contrib.auth.models import User
from main.models import UserMap, Pin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import password_validation


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
    lat = forms.CharField()
    long = forms.CharField()
    notes = forms.CharField(widget=forms.Textarea, max_length=1500, required=False) 


# Form for updating email 
class UpdateEmail(ModelForm):
    email = forms.CharField(max_length=50, min_length=4)

    class Meta:
        model = User
        fields = ['email',]  

# Form for changing password 

class ChangePassword(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Current Password",
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        required=True,
        validators=[password_validation.validate_password]
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password",
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            self.add_error('confirm_new_password', "New passwords do not match.")

class AccountDeletionForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Enter your password to confirm')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if self.user and not self.user.check_password(password):
            raise forms.ValidationError("Password is incorrect")
        return password
    
