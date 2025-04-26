from booking.views import gp_info, appointment, show_appointments, cancel_appointment, edit_appointment, show_patients_appointments
from django.urls import path
from .views import home, signup, signin, gp
from django.shortcuts import redirect

app_name = "booking"
urlpatterns = [
    path('', lambda request: redirect('booking:home', permanent=False)),
    path('home/', view=home, name='home'),
    path('signup/', view=signup, name='signup'),
    path('signin/', view=signin, name='signin'),
    path('gp/', view=gp, name='gp'),

    path('gp_info/<int:doctor_id>', view=gp_info, name='gp_info'),

    path('appointment/<int:doctor_id>/<int:patient_id>', view=appointment, name='book-appointment'),

    path('appointment/<int:doctor_id>/', view=show_appointments, name='show-appointments'),

    path('appointment_cancel/<int:appointment_id>', view=cancel_appointment, name='cancel_appointment'),

    path('appointment_edit/<int:appointment_id>/<int:doctor_id>/<int:slot_id>/', view=edit_appointment, name='edit_appointment'),

    path('appointment_edit_patient/<int:patient_id>/', view=show_patients_appointments, name='show_patients_appointments'),
]