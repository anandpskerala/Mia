from pyrogram import Client, filters
from pyrogram.types import Message

from mia import CONFIG
from mia.modules.localization import tld


@Client.on_message(filters.command("start", prefixes=CONFIG.prefixes))
async def start_menu(c: Client, m: Message):
    bot = await c.get_me()
    await m.reply_text(
        tld(m.chat.id, "start_text").format(m.from_user.first_name, bot.first_name),
        quote=True
    )
