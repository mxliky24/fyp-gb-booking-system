from chatapp.views import get_messages, post_message
from django.urls import path

app_name="chatapp"
urlpatterns = [
    path('get_messages/<str:email>/', view=get_messages, name="get_messages"),
    path('make_message/<str:email>/', view=post_message, name="make_messages")
]