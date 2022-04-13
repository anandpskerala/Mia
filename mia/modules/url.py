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


@Client.on_message(filters.command("unshort", prefixes=CONFIG.prefixes))
async def unshorten_url(c: Client, m: Message):
    chat = m.chat

    if len(m.command) < 2:
        await m.reply_text(
            tl(chat.id, "no_url_found"),
            quote=True
        )
    else:
        url = m.text.split(maxsplit=1)[1]
        if not url.startswith("https"):
            url = "https://" + url

        async with aiohttp.ClientSession() as client:
            async with client.get(url, allow_redirects=False) as result:
                if str(result.status).startswith("3"):
                    text = tl(chat.id, "unshortened_url").format(url=url, r_url=result.headers.get('Location'))
                else:
                    text = tl(chat.id, "unshorten_unsuccessful").format(url=url, status=result.status)
                await m.reply_text(
                    text,
                    quote=True
                )

