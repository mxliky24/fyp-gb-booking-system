from django.db import models

# Stores basic user info for chat
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100) # User’s display name
    email = models.EmailField(unique=True) # Used to identify chat sessions per user
# Stores each message with sender info and links it to a user
class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Associates message with user
    sender = models.CharField(max_length=255) # Indicates if message is from user or chatbot
    message_text = models.TextField()  # Actual message content

    # Converts message into dictionary format for JSON responses
    def serialize(self):
        return {
            "sender": self.sender,
            "message_text": self.message_text
        }
