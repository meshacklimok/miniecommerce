from django.contrib import admin
from .models import HelpCategory, FAQ, SupportTicket, ContactMessage

admin.site.register(HelpCategory)
admin.site.register(FAQ)
admin.site.register(SupportTicket)
admin.site.register(ContactMessage)

