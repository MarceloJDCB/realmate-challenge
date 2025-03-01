from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'created_at', 'updated_at')
    list_filter = ('state', 'created_at', 'updated_at')
    search_fields = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'direction', 'timestamp', 'created_at')
    list_filter = ('direction', 'timestamp', 'created_at')
    search_fields = ('id', 'content', 'conversation__id')
    readonly_fields = ('created_at',)
    ordering = ('-timestamp',)
    raw_id_fields = ('conversation',)
