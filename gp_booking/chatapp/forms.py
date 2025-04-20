from django import forms

class MessageForm(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea)
