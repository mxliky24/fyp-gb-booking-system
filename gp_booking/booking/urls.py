from django.urls import path
from .views import home, signup, signin

urlpatterns = [
    path('home/', view=home, name='home'),
    path('signup/', view=signup, name='signup'),
    path('signin/', view=signin, name='signin'),
]