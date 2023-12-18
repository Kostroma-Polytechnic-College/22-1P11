from django.contrib.admin import ModelAdmin, register
from app.models import *

@register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ('id', 'uid', 'name', 'is_admin')

@register(Travel)
class TravelUserAdmin(ModelAdmin):
    list_display = ('user', 'start_datetime', 'end_datetime')