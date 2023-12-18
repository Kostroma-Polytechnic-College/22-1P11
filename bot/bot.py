import asyncio
import re
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, KeyboardButton, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup
from .secret import TELEGRAM_TOKEN as token
from . import navigation as nav
from app.models import TelegramUser
from django.core.exceptions import ObjectDoesNotExist

from asgiref.sync import sync_to_async

bot = Bot(token=token)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop) 
    
@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message):
    user, created = TelegramUser.objects.get_or_create(uid=message.from_user.id)
    if created:
        user.name = message.from_user.username

    context = eval(user.context)
    context["state"] = 1
    context["new_state"] = 1
    context['user_id'] = user.uid
    user.context = str(context)

    user.save()
    await send(user)


@dp.callback_query_handler(lambda callback_query: callback_query.data)
async def callback_query(callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
    except Exception:
        pass

    context = eval(callback_query.data)

    user = TelegramUser.objects.get_or_create(uid=callback_query.from_user.id)[0]
    await send(user, **eval(callback_query.data))


async def send_admin(dp):
    try:
        admin = TelegramUser.objects.get(is_admin=True)

        await bot.send_message(
            chat_id=admin.uid, 
            text="Бот запущен!")
    except ObjectDoesNotExist:
        print("В БД должен быь один админ")

async def send(user:TelegramUser, **kwargs):
    context = eval(user.context)
    context.update(kwargs)

    text, reply_markup = nav.get_reply_message(context)
    await bot.send_message(
        chat_id=user.uid,
        text=text,
        reply_markup=reply_markup)

def run():
    executor.start_polling(
        dispatcher=dp, 
        on_startup=send_admin)

if __name__ == '__main__':
    run()