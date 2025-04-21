from logging import raiseExceptions

from django.core.signals import request_started
from django.http import HttpResponse, Http404
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

def show_appointments(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if doctor is not None:
        doctor_slots =  doctor.slot_set.all()
        if len(doctor_slots) > 0:
            return render(request=request, template_name="doctor/appointments.html", context={'slots' : doctor_slots})
        else:
            return render(request=request, template_name='doctor/appointments.html', context={'slots': []})
    else:
        raiseExceptions(f"Could not find doctor with Id f{doctor_id}")

def cancel_appointment(request, appointment_id):
    if request.method == "DELETE":
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = "Cancelled"
        appointment.save()
        return redirect('show_appointments', doctor_id=appointment.slot.doctor_id)

def edit_appointment(request, doctor_id, appointment_id, slot_id):
    if request.method == "PUT":
        slot = Slot.objects.get(id=slot_id)
        appointment = Appointment.objects.get(id=appointment_id)
        doctor = Doctor.objects.get(id=doctor_id)
        if slot is not None and appointment is not None and doctor is not None:
            appointment.slot = slot
            appointment.save()
            return redirect('show_appointments', doctor_id=appointment.slot.doctor_id)
    else:
        doctor = Doctor.objects.get(id=doctor_id)
        appointment = Appointment.objects.get(id=appointment_id)
        if doctor is not None and appointment is not None:
            slots = doctor.slot_set.exclude(id=slot_id)
            if len(slots) > 0:
                return render(request=request, template_name="doctor/edit_appointment.html", context={'slots' : slots, 'appointment' : appointment, 'doctor' : doctor})
            else:
                raiseExceptions("The slots cannot be empty")
        else:
            raiseExceptions("Doctor or Appointment cannot be none")

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