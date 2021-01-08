from django.contrib import admin

# Register your models here.

from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'dt_sending', 'chat_id', 'recipient_id', 'sender_id')
    list_display_links = ('id',)
    search_fields = ('text', 'content', 'sender_id', 'recipient_id')


class ChatAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_display = ('id', 'title', 'user1_id', 'user2_id')
    search_fields = ('user1_id', 'user2_id')


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)