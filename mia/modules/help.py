from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules.localization import tl


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
        button = [
            [
                InlineKeyboardButton(tl(chat.id, "back"), callback_data="start_back")
            ]
        ]
        markup = InlineKeyboardMarkup(button)
        text = tl(chat.id, "help_text")
    await method(text, reply_markup=markup)
