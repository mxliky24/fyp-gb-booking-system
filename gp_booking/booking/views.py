from django.shortcuts import render, redirect
from .models import Appointment, Doctor, Patient
from .forms import SignupForm, LoginForm

# Create your views here.
def home(request):
    return render(request=request, template_name='home.html')

def gp(request):
    doctors = Doctor.objects.all()

def signup(request):
    form = SignupForm()

    return render(request=request, template_name='signup.html', context={'form': form})

def signin(request):
    form = LoginForm()

    return render(request=request, template_name='signin.html', context={'form': form})

def appointment(request):
    pass


