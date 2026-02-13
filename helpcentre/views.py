from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import HelpCategory, FAQ, SupportTicket, TicketReply
from .forms import TicketForm, ReplyForm, ContactForm


# ----- HELP CENTER -----
def help_centre(request):
    query = request.GET.get('q')
    faqs = FAQ.objects.filter(is_active=True)
    if query:
        faqs = faqs.filter(question__icontains=query)
    categories = HelpCategory.objects.all()
    return render(request, 'helpcentre/help_centre.html', {
        'faqs': faqs,
        'categories': categories,
    })


# ----- CONTACT SUPPORT -----
def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Notify admin
            send_mail(
                'New Contact Message',
                'A customer sent a contact message.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )
            return redirect('helpcentre:help_centre')
    else:
        form = ContactForm()
    return render(request, 'helpcentre/contact.html', {'form': form})


# ----- SUBMIT TICKET -----
@login_required
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Email notifications
            if request.user.email:
                send_mail(
                    'Support Ticket Received',
                    f'Your ticket #{ticket.id} has been received.',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                )
            send_mail(
                'New Support Ticket',
                f'New ticket #{ticket.id} from {request.user.username}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )
            return redirect('helpcentre:my_tickets')
    else:
        form = TicketForm()
    return render(request, 'helpcentre/ticket.html', {'form': form})


# ----- MY TICKETS -----
@login_required
def my_tickets(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'helpcentre/my_tickets.html', {
        'tickets': tickets,
        'whatsapp_number': settings.WHATSAPP_SUPPORT_NUMBER,
    })


# ----- TICKET DETAIL (CHAT STYLE) -----
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    replies = ticket.replies.all().order_by('created_at')

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            reply.save()

            # Notify admin
            send_mail(
                f'Ticket #{ticket.id} New Reply',
                f'{request.user.username} replied to ticket #{ticket.id}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )

            return redirect('helpcentre:ticket_detail', ticket_id=ticket.id)
    else:
        form = ReplyForm()

    return render(request, 'helpcentre/ticket_detail.html', {
        'ticket': ticket,
        'replies': replies,
        'form': form,
        'whatsapp_number': settings.WHATSAPP_SUPPORT_NUMBER,
    })



