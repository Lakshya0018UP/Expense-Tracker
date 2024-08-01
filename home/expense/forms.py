from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    income = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'income']
