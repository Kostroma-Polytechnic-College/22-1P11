import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from . import navigation as nav
from .secret import TELEGRAM_TOKEN as token
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Телеграмм бот"

    def handle(self, *args, **options):

        bot = Bot(token=token)
        loop = asyncio.get_event_loop()
        dp = Dispatcher(bot, loop=loop)


        @dp.message_handler(commands=["start"])
        async def command_start_handler(message: Message):
            text, reply_markup = nav.get_reply_message({'new_state':1})
            await bot.send_message(
                chat_id=message.from_user.id,
                text=text,
                reply_markup=reply_markup)


        @dp.callback_query_handler(lambda callback_query: callback_query.data)
        async def callback_query(callback_query: CallbackQuery):
            context = eval(callback_query.data)
            if context['new_state'] == 1:
                text, reply_markup = nav.get_reply_message(context)
                await bot.send_message(
                    chat_id=callback_query.from_user.id,
                    text=text,
                    reply_markup=reply_markup)
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

        @dp.message_handler()
        async def messages(message: Message):    
            text, reply_markup = nav.get_reply_message({'new_state':1})
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=text,
                reply_markup=reply_markup)
        
        executor.start_polling(dispatcher=dp)