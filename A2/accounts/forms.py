from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    error_messages = {
        "invalid_login": "Username or password is invalid"
    }

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 
                  'last_name']

    def clean_username(self):
        data = self.cleaned_data["username"]
        
        if not data:
            raise ValidationError(
                "This field is required"
            )
        
        if User.objects.filter(username=data).exists():
            raise ValidationError(
                "A user with that username already exists"
            )
        
        return data

    def clean_password1(self):
        data = self.cleaned_data["password1"]
        
        if not data:
            raise ValidationError(
                "This field is required"
            )

        if len(data) < 8:
            raise ValidationError(
                "This password is too short. It must contain at least 8 characters"
            )
        return data
    
    def clean_password2(self):
        data1 = self.cleaned_data.get("password1")
        data2 = self.cleaned_data.get("password2")

        if data1 and data2:
            if data1 != data2:
                raise ValidationError(
                    "The two password fields didn't match"
                )

        if not data2:
            raise ValidationError(
                "This field is required"
            )
        
        if len(data2) < 8:
            raise ValidationError(
                "This password is too short. It must contain at least 8 characters"
            )
        
        return data2
    
    def clean_email(self):
        data = self.cleaned_data["email"]

        if data:
            try:
                validate_email(data)
            except ValidationError as e:
                raise ValidationError(
                    "Enter a valid email address"
                )
            
        return data

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    #password1 = forms.PasswordInput()
    #password2 = forms.PasswordInput()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
