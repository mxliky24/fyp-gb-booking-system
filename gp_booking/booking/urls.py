from django.urls import path
from .views import home, signup, signin, gp

urlpatterns = [
    path('home/', view=home, name='home'),
    path('signup/', view=signup, name='signup'),
    path('signin/', view=signin, name='signin'),
    path('gp/', view=gp, name='gp'),
]