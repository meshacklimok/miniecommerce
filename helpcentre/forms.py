from django import forms
from .models import SupportTicket, TicketReply, ContactMessage

class TicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['message']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']



# Contact us form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

