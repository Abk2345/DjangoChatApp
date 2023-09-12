from django.contrib import admin

# Register your models here.

from .models import Room, Message, PersonalMessage

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PersonalMessage)
