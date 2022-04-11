import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

from mia import CONFIG
from mia.modules.localization import tl


@Client.on_message(filters.command("short", prefixes=CONFIG.prefixes))
async def shorten_url(c: Client, m: Message):
    chat = m.chat

    if len(m.command) < 2:
        await m.reply_text(
            tl(chat.id, "no_url_found"),
            quote=True
        )
    else:
        url = m.text.split(maxsplit=1)[1]
        sample_url = "https://da.gd/s?url={}".format(url)
        async with aiohttp.ClientSession() as client:
            result = await (await client.get(sample_url)).text()

        if result:
            text = tl(chat.id, "shortened_url").format(url=url, short_url=result)
        else:
            text = tl(chat.id, "something_wrong")
        await m.reply_text(
            text,
            quote=True
        )

