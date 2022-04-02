from typing import Union
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mia import CONFIG
from mia.modules.localization import tl, locale_codes, lang_strings


def gen_langs_kb():
    langs = locale_codes
    kb = []
    while langs:
        lang = lang_strings[langs[0]]
        a = [
            InlineKeyboardButton(
                f"{lang['language_flag']} {lang['language_name']}",
                callback_data="set_lang " + langs[0],
            )
        ]
        langs.pop(0)
        if langs:
            lang = lang_strings[langs[0]]
            a.append(
                InlineKeyboardButton(
                    f"{lang['language_flag']} {lang['language_name']}",
                    callback_data="set_lang " + langs[0],
                )
            )
            langs.pop(0)
        kb.append(a)
    return kb


@Client.on_message(filters.command("lang", prefixes=CONFIG.prefixes))
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
