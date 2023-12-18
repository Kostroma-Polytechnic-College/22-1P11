from django.core.management.base import BaseCommand
from bot import bot

class Command(BaseCommand):
    help = "Телеграмм бот"

    def handle(self, *args, **options):
        bot.run()