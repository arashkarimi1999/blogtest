from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from apps.user_module.models import User


class RegisterForm(forms.Form):

    first_name=forms.CharField(
        label="first_name",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "firstname",
            'name': 'firstname',
            'type': "firstname"
        }))

    last_name=forms.CharField(
        label="last_name",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "lastname",
            'name': 'lastname',
            'type': "lastname"
        }))
    
    phone_number=forms.CharField(
        label="phone_number",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "phonenumber",
            'name': 'phonenumber',
            'type': "phonenumber"
        }))

    email = forms.CharField(
        label="email",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "email",
            'name': 'email',
            'type': "email"
        }))
    
    password = forms.CharField(
        label='password ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "password ",
        }))
    
    confirm_password = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "password confirmation",
        }))
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
    
    # avatar=forms.FileField(label="avatar")


    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user: User = User.objects.filter(username__iexact=username)
    #
    #     if user :
    #         raise ValidationError('کاربری با این نام وجود دارد')


class LoginForm(forms.Form):
    
    email = forms.EmailField(
        label='email addres ',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'type': "email",
            'placeholder': "email address",
        }))
    
    password = forms.CharField(
        label='password  ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "password",
        }))


class ForgetPassForm(forms.Form):

    email = forms.EmailField(
        label='email address  ',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'type': "email",
            'placeholder': "email address",
        }))


class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        label='new password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "new password",
        }))
    
    confirm_password = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': " password confirmation",
        }))
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')


class EditPanelForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','number','avatar']
        
        widgets = {
            'first_name': forms.TextInput( attrs={
                'class': "req",
                'placeholder': "name  ",
                'name': 'name',
                'type': "text"
            }),
            'last_name': forms.TextInput(attrs={
                'class': "req",
                'placeholder': "lastname   ",
                'name': 'name',
                'type': "text"
            }),

            'number': forms.NumberInput(attrs={
                'class': "req",
                'placeholder': "mobile phone  ",
                'name': 'text',
                'type': "text"
            }),
            "avatar" : forms.FileInput()



        }
        labels = {
            'first_name': ' first_name',
            'last_name': ' last_name ',
            'username': 'username',
            'number': 'number',
            'avatar' : 'avatar',

        }


class EditPasswordForm(forms.Form):

    current_password = forms.CharField(
        label='current password ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "current password",
        }))
    
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "password",
        }))

    confirm_password = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': "password",
            'placeholder': "password confirmation",
        }))
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')