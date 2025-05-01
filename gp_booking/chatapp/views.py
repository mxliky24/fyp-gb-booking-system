from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import User, Message
from chatapp.forms import MessageForm
from chatapp.chat_service import generate_response

chatbot_sender_name = "chat bot"
# Displays chat messages for a given user, or creates a new user if not found
def get_messages(request, email):
    form = MessageForm()
    user = get_user(email=email) # Looks up user by email
    print(user)
    if user is not None:
        user_messages = user.message_set.all() # Retrieves all previous messages for user
        if len(user_messages) > 0:
            return render(request, "chat.html", context= {"user_messages" : user_messages, "form" : form})
        return render(request, 'chat.html', context={"user_messages" : [], "form" : form})
    # If user does not exist, create one using logged-in user's name
    new_user = User()
    new_user.name = f"{request.user.first_name} {request.user.last_name}"
    new_user.email = email
    user_messages = new_user.message_set
    new_user.save()
    return render(request=request, template_name='chat.html', context={"user_messages" : [], "form" : form})
# Helper method to safely retrieve user object by email
def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

# Handles form submission and stores both user and chatbot messages
def post_message(request, email):
    if request.method == 'POST':
        user = User.objects.get(email = email)
        user_input = MessageForm(request.POST)  # Form containing user’s new message
        print(user_input)
        if user_input.is_valid():
            print('valid input')
            if user is not None:
                print('adding new message')
                new_message = Message.objects.create(user=user) # Creates message by user
                new_message.message_text = user_input.cleaned_data['message_text']
                new_message.sender = user.name
                new_message.save()
                # Generates chatbot response and saves it
                chat_response = Message.objects.create(user=user)
                chat_response.sender = chatbot_sender_name
                chat_response.message_text =  generate_response(user_input.cleaned_data['message_text']) 
                chat_response.save()

                message_set = [new_message, chat_response]
                # Returns both user and chatbot messages as JSON
                return JsonResponse({
                    "new_messages" : message.serialize() for message in message_set
                })
        else:
            raise Exception('invalid form')




