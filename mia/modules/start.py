from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules.localization import tl


@Client.on_message(filters.command("start", prefixes=CONFIG.prefixes))
@Client.on_callback_query(filters.regex("^start_back$"))
async def start_menu(c: Client, m: Union[Message, CallbackQuery]):
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
        await method(
            tl(chat.id, "group_start")
        )
    else:
        bot = await c.get_me()
        buttons = [
            [
                InlineKeyboardButton(tl(chat.id, "help"), callback_data="get_help")
            ],
            [
                InlineKeyboardButton(tl(chat.id, "support_grp"), url="https://t.me/Mia_support"),
                InlineKeyboardButton(tl(chat.id, "support_chnl"), url="https://t.me/KeralaBotsNews")
            ]
        ]
        markup = InlineKeyboardMarkup(buttons)
        await method(
            tl(chat.id, "start_text").format(m.from_user.first_name, bot.first_name),
            reply_markup=markup
        )
