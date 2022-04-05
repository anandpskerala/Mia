from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules.localization import tl, gen_langs_kb
from mia.database.langs import update_lang


@Client.on_message(filters.command("setlang", prefixes=CONFIG.prefixes))
@Client.on_callback_query(filters.regex("^get_lang$"))
async def get_lang_menu(c: Client, m: Union[Message, CallbackQuery]):

    if isinstance(m, CallbackQuery):
        await m.answer()
        msg = m.message
        method = m.edit_message_text
        chat = m.message.chat
    else:
        msg = m
        method = m.reply_text
        chat = m.chat
    keyboard = gen_langs_kb()
    keyboard.append(
        [
            InlineKeyboardButton(
                tl(chat.id, "back"),
                callback_data="start_back"
            )
        ]
    )
    text = tl(chat.id, "change_language")
    await method(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("^setlang_.*"))
async def get_lang_menu(c: Client, m: CallbackQuery):
    _, lang = m.data.split("_", 1)
    await m.answer()
    msg = m.message
    chat = m.message.chat
    update_lang(str(chat.id), lang)

    keyboard = [
        [
            InlineKeyboardButton(
                tl(chat.id, "back"),
                callback_data="get_lang"
            )
        ]
    ]

    text = tl(chat.id, "changed_language").format(f"{tl(chat.id, 'language_flag')} {tl(chat.id, 'language_name')}")
    await m.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
