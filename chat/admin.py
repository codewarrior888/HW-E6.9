from django.contrib import admin

# Register your models here.

from .models import Account, Message, Room

admin.site.register(Account)
admin.site.register(Message)
admin.site.register(Room)
