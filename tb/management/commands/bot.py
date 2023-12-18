import asyncio
import re
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, KeyboardButton, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup
from .secret import TELEGRAM_TOKEN as token
from . import navigation as nav
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from tb.models import TelegramUser as TUser

class Command(BaseCommand):
    help = "Телеграмм бот"

    def handle(self, *args, **options):
        bot = Bot(token=token)
        loop = asyncio.get_event_loop()
        dp = Dispatcher(bot, loop=loop)

        @dp.message_handler(commands=["start"])
        async def command_start_handler(message: Message):
            await main_menu(message.from_user.id)

        @dp.message_handler(content_types=['document'])
        async def document(message):
            await message.document.download()
            

        @dp.message_handler()
        async def messages(message: Message):
            pass


        async def main_menu(chat_id):
            text, reply_markup = nav.get_reply_message({'new_state':1})
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup)

        @dp.callback_query_handler(lambda callback_query: callback_query.data)
        async def callback_query(callback_query: CallbackQuery):
            try:
                await callback_query.message.delete()
            except Exception:
                pass

            context = eval(callback_query.data)

            if context['new_state'] == 1:
                await main_menu(callback_query.from_user.id)
            elif context['new_state'] == 11:
                text, reply_markup = nav.get_reply_message(context)
                await bot.send_message(
                    chat_id=callback_query.from_user.id,
                    text=text,
                    reply_markup=reply_markup)
            elif context['new_state'] == 12:
                text, reply_markup = nav.get_reply_message(context)
                await bot.send_message(
                    chat_id=callback_query.from_user.id,
                    text=text,
                    reply_markup=reply_markup)

        @sync_to_async
        def get_admin():
            return TUser.objects.get(is_admin=True)

        async def send_admin(dp):
            admin = await get_admin()
            await bot.send_message(
                chat_id=admin.external_id, 
                text="Бот запущен!")

        executor.start_polling(dispatcher=dp, on_startup=send_admin)
    