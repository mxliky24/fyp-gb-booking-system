from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import User, Message
from chatapp.forms import MessageForm
from chatapp.chat_service import generate_response

chatbot_sender_name = "chat bot"
# Create your views here.
def get_messages(request, email):
    form = MessageForm()
    user = get_user(email=email)
    print(user)
    if user is not None:
        user_messages = user.message_set.all()
        if len(user_messages) > 0:
            return render(request, "chat.html", context= {"user_messages" : user_messages, "form" : form})
        return render(request, 'chat.html', context={"user_messages" : [], "form" : form})
    new_user = User()
    new_user.name = f"{request.user.first_name} {request.user.last_name}"
    new_user.email = email
    user_messages = new_user.message_set
    new_user.save()
    return render(request=request, template_name='chat.html', context={"user_messages" : [], "form" : form})

def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def post_message(request, email):
    if request.method == 'POST':
        user = User.objects.get(email = email)
        user_input = MessageForm(request.POST)
        print(user_input)
        if user_input.is_valid():
            print('valid input')
            if user is not None:
                print('adding new message')
                new_message = Message.objects.create(user=user)
                new_message.message_text = user_input.cleaned_data['message_text']
                new_message.sender = user.name
                new_message.save()
                chat_response = Message.objects.create(user=user)
                chat_response.sender = chatbot_sender_name
                chat_response.message_text =  generate_response(user_input.cleaned_data['message_text']) 
                chat_response.save()

                message_set = [new_message, chat_response]

                return JsonResponse({
                    "new_messages" : message.serialize() for message in message_set
                })
        else:
            raise Exception('invalid form')




