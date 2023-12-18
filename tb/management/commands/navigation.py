from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from yaml import Loader, load
import os
from tb.models import *
from datetime import timezone as tz
from datetime import datetime as dt
from datetime import timedelta as td

MENU = load(open(
    os.path.join(os.getcwd(), 'tb', 'management', 'commands', 'navigation.yml'), 
    'r', encoding='utf-8'), Loader=Loader)

def get_static_buttons(context: dict):
    buttons = []
    state = context["new_state"]
    if 'static_buttons' not in MENU[state]:
        return buttons
    for button_text, params in MENU[state]["static_buttons"].items():
        callback_data = {'new_state': params['new_state']}
        buttons.append(InlineKeyboardButton(
            text=button_text,
            callback_data=str(callback_data)))
    return buttons

def get_dynamic_buttons(context: dict):
    buttons = []
    state = context['new_state']
    if 'dynamic_buttons' not in MENU[state]:
        return buttons
    dynamic_buttons = MENU[state]['dynamic_buttons']
    query = dynamic_buttons['query']
    
    for item in eval(query.format(**context)):
        button_content = eval(f"item.{dynamic_buttons['field']}")
        context[dynamic_buttons['id_arg']] = item.id
        context['text'] = button_content
        callback_data = {
            'new_state': dynamic_buttons['new_state'],
            dynamic_buttons['id_arg']: item.id}
        buttons.append(InlineKeyboardButton(
            text=button_content, 
            callback_data=str(callback_data)))
    return buttons



def get_conditional_buttons(context: dict):
    buttons = []
    state = context['new_state']
    if 'conditional_buttons' not in MENU[state]:
        return buttons
    for button_text, params in MENU[state]["conditional_buttons"].items():
        try:
            result = eval(params['condition'].format(**context))
            if result:
                callback_data = {'new_state': params['new_state']}
                buttons.append(InlineKeyboardButton(
                    text=button_text,
                    callback_data=str(callback_data)))
        except Exception as ex:
            print(ex)

    return buttons

def get_reply_message(context: dict):
    inline_keyboard = []
    row = []
    for button in  get_dynamic_buttons(context):
        row.append(button)
        if len(row) == 1:
            inline_keyboard.append(row)
            row = []
    if len(row) > 0:
        inline_keyboard.append(row)

    inline_keyboard.append(get_conditional_buttons(context))
    
    inline_keyboard.append(get_static_buttons(context))
    
    markup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=inline_keyboard)

    text = eval(MENU[context['new_state']]['message'].format(**context))
    return text, markup
