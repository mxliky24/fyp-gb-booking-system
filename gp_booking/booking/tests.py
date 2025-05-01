from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from booking.models import CustomUser, Doctor, Patient, Appointment, Slot
from django.contrib.auth.hashers import make_password

# Integration test to verify appointment booking logic
class TestUserAppointmentIntegrationTest(TestCase):

    # Sets up test data: doctor, patient, and booked slot
    def setUp(self):
        self.user_doctor = CustomUser.objects.create(username='testdoctor', password=make_password('123123'),
                                                     email='test@doctor.co.uk')  # Ensures password is hashed
        self.user_patient = CustomUser.objects.create(username='testpatient', password=make_password('123123'),
                                                      email='test@patient.co.uk')
        self.doctor = Doctor.objects.create(user=self.user_doctor, speciality='Surgeon', price=100.50)
        self.doctor.speciality = 'Surgeon'
        self.patient = Patient.objects.create(user=self.user_patient)
        self.slot = Slot.objects.create(doctor=self.doctor, date=datetime.now(), time=datetime.now().time(),
                                        is_booked=True) # Simulates a slot that is already booked

    # Verifies that an appointment links to a booked slot
    def test_book_appointment(self):
        self.appointments = Appointment.objects.create(patient=self.patient, slot=self.slot, status='Pending')
        self.assertTrue(self.appointments.slot.is_booked)  # Confirms booking status remains true
