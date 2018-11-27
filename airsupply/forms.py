from django.contrib.auth.models import User
from .models import Place
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name']

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do no match"
            )
        return confirm_password


class ClinicManagerForm(UserForm):
    clinicName = forms.ModelChoiceField(queryset=Place.objects.exclude(name='Queen Mary Hospital Drone Port'))

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'clinicName']


class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="New password", required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Retype New password", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != "" and password != confirm_password:
            raise forms.ValidationError(
                "Passwords do no match"
            )
        return confirm_password
