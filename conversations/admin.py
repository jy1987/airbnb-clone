from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Conversation Admin definition"""

    pass


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """Message Admin definition"""

    pass
