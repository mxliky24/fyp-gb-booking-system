from booking.models import Doctor, Patient
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class SignupForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'password']

class AddDoctorForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'password', 'picture']

class EditDoctorForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'password', 'picture']



