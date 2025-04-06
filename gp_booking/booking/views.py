from lib2to3.fixes.fix_input import context
from logging import raiseExceptions

from django.core.signals import request_started
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Appointment, Doctor, Patient, Role, Slot
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request=request, template_name='home.html')

def gp(request):
    doctors = Doctor.objects.all()
    return render(request=request, template_name='gp.html', context={'doctors': doctors})


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if  form.is_valid():
            print("form is valid")
            new_patient = form.save()
            new_patient.username = new_patient.email
            new_patient.save()
            role = Role.objects.get(name='PATIENT')
            role.customuser_set.add(new_patient)
            role.save()
            login(request, new_patient)
            return render(request, template_name='home.html', context={'patient': new_patient})

        else:
            print("form is invalid")
            return render(request=request, template_name='signup.html', context={'form_errors': form.errors, 'form': form})

    return render(request=request, template_name='signup.html', context={'form': form})

def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data.get('email')
        password = form.data.get('password')
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role.name == 'DOCTOR':
                return render(request, template_name='home.html', context={'doctor': user})
            else:
                return render(request, template_name='home.html', context={'patient': user})

        else:
            return HttpResponse('Invalid login or password')

    return render(request=request, template_name='signin.html', context={'form': form})

def gp_info(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request=request, template_name="gp_info.html", context={'doctor': doctor})

def appointment(request, doctor_id, patient_id):
    if request.method == 'POST':
        patient = Patient.objects.get(user_id=patient_id)
        slot_id = request.POST.get('slot_id')
        if slot_id is None:
            messages.error(request, "Please choose a slot to book an appointment")
            return redirect('gp_info', doctor_id=doctor_id)
        slot = Slot.objects.get(id=slot_id)
        slot.is_booked = True
        slot.save()
        appointment = Appointment()
        appointment.patient = patient
        appointment.slot = slot
        appointment.status = 'Confirmed'
        appointment.save()
        messages.success(request, "Your appointment has been booked")
        return redirect('gp_info', doctor_id=doctor_id)

