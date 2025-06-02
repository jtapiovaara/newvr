from django.contrib import admin

from justchat.models import Chat, ChatImage


# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatImage)
class ChatImageAdmin(admin.ModelAdmin):
    pass