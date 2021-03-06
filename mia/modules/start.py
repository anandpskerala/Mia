from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules.localization import tl
from mia.database.users import insert_user, get_user


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
    user = msg.from_user
    insert_user(str(user.id), user.username, str(user.dc_id))
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
                InlineKeyboardButton(tl(chat.id, "support_grp"), url="https://t.me/KeralasBots"),
                InlineKeyboardButton(tl(chat.id, "support_chnl"), url="https://t.me/KeralaBotsNews")
            ],
            [
                InlineKeyboardButton(f'{tl(chat.id, "language_flag")} {tl(chat.id, "language_string")}'
                                     , callback_data="get_lang")
            ]
        ]
        markup = InlineKeyboardMarkup(buttons)
        await method(
            tl(chat.id, "start_text").format(m.from_user.first_name, bot.first_name),
            reply_markup=markup
        )
