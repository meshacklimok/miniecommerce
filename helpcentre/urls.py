from django.urls import path
from .views import (
    help_centre,
    contact_support,
    submit_ticket,
    my_tickets,
    ticket_detail
)

app_name = 'helpcentre'

urlpatterns = [
    path('', help_centre, name='help_centre'),
    path('contact/', contact_support, name='contact_support'),
    path('ticket/new/', submit_ticket, name='submit_ticket'),
    path('tickets/', my_tickets, name='my_tickets'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
]

