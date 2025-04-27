from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from booking.models import CustomUser, Doctor, Patient, Appointment, Slot
from django.contrib.auth.hashers import make_password


def UserAppointmentIntegrationTest(TestCase):

    def setup(self):
        self.user_doctor = CustomUser.objects.create(username='testdoctor', password=make_password('123123'), email='test@doctor.co.uk')
        self.user_patient = CustomUser.objects.create(username='testpatient', password=make_password('123123'), email='test@patient.co.uk')
        self.doctor = Doctor.objects.create(user=self.user_doctor)
        self.doctor.speciality = 'Surgeon'
        self.patient = Patient.objects.create(user=self.user_patient)

    def set_doctor_slots(self):
        self.slot = Slot.objects.create(doctor=self.doctor, date=datetime.now(), time=datetime.now().time(), is_booked=True)
    def book_appointment(self):
        self.appointments = Appointment.objects.create(patient=self.doctor_patient, slot=self.slot, status= 'Pending')

