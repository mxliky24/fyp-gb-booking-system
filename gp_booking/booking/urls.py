from booking.views import gp_info, appointment
from django.urls import path
from .views import home, signup, signin, gp
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home', permanent=False)),
    path('home/', view=home, name='home'),
    path('signup/', view=signup, name='signup'),
    path('signin/', view=signin, name='signin'),
    path('gp/', view=gp, name='gp'),

    path('gp_info/<int:doctor_id>', view=gp_info, name='gp_info'),

    path('appointment/<int:doctor_id>/<int:patient_id>', view=appointment, name='appointment'),
]