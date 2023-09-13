from django.contrib import admin
from .models import Room, Message, PersonalMessage

# for Handling from admin, registering all the models
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(PersonalMessage)
