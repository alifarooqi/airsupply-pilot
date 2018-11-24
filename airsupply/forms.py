from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField()

    class Meta:
        model = User
        fields = ['role', 'username', 'email', 'password', 'first_name', 'last_name']


class ClinicManagerForm(UserForm):
    clinicName = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'clinicName']

