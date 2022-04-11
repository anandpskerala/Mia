from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules import MODULES
from mia.modules.localization import tl


def gen_help_kb(chat_id):
    keyboards = [InlineKeyboardButton(
        tl(chat_id, f"{x}_menu_text"),
        callback_data=f"help_{x}") for x in MODULES if x not in ['help', 'start']]

    pairs = []
    pair = []

    for module in keyboards:
        pair.append(module)
        if len(pair) > 2:
            pairs.append(pair)
            pair = []

    if pair:
        pairs.append(pair)

    return pairs


@Client.on_message(filters.command("help", prefixes=CONFIG.prefixes))
@Client.on_callback_query(filters.regex("^get_help$"))
async def get_help_menu(c: Client, m: Union[Message, CallbackQuery]):
    bot = await c.get_me()
    if isinstance(m, CallbackQuery):
        await m.answer()
        msg = m.message
        method = m.edit_message_text
        chat = m.message.chat
    else:
        msg = m
        method = m.reply_text
        chat = m.chat

    if chat.type != "private":
        button = [
            [
                InlineKeyboardButton(
                    tl(chat.id, "help"),
                    url=f'https://t.me/{bot.username}?start=start'
                )
            ]
        ]

        markup = InlineKeyboardMarkup(button)
        text = tl(chat.id, "group_help")
    else:
        button = gen_help_kb(chat.id)
        button.append(
            [
                InlineKeyboardButton(tl(chat.id, "back"), callback_data="start_back")
            ]
        )
        markup = InlineKeyboardMarkup(button)
        text = tl(chat.id, "help_text").format(botname=bot.first_name)
    await method(text, reply_markup=markup)
