from pyrogram import Client, filters
from pyrogram.types import Message

from mia import CONFIG
from mia.modules.localization import tld


@Client.on_message(filters.command("start", prefixes=CONFIG.prefixes))
async def start_menu(c: Client, m: Message):
    chat = m.chat
    if chat.type != "private":
        await m.reply_text(
            tld(chat.id, "private_start"),
            quote=True
        )
    else:
        bot = await c.get_me()
        await m.reply_text(
            tld(chat.id, "start_text").format(m.from_user.first_name, bot.first_name),
            quote=True
        )
