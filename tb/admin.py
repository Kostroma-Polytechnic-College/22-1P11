from django.contrib.admin import ModelAdmin, register
from tb.models import TelegramUser

@register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'is_admin')