from booking.models import Doctor, Patient, CustomUser
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class SignupForm(CustomUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # optional: avoid blank username errors
        if commit:
            user.save()
            Patient.objects.create(user=user, phone=self.cleaned_data.get('phone'))
        return user






