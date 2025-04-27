from booking.models import Doctor, Patient, CustomUser, Appointment, Slot
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def __int__(self, *args, **kwargs):

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

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
    
class DoctorAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['slot', 'status']

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        current_slot = kwargs.pop('current_slot', None)

        super().__init__(*args, **kwargs)

        available_slots = Slot.objects.filter(doctor=doctor, is_booked=False)
        if current_slot and current_slot not in available_slots:
            available_slots = available_slots | Slot.objects.filter(pk=current_slot.pk)

        self.fields['slot'].queryset = available_slots
        self.fields['slot'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})









