from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message_text = models.TextField()

    def serialize(self):
        return {
            "sender": self.sender,
            "message_text": self.message_text
        }
