from pyrogram import Client, filters
from pyrogram.types import Message

from mia import CONFIG
from mia.modules.localization import tl
from mia.utils.admins import admin_check


@Client.on_message(filters.command("pin", prefixes=CONFIG.prefixes))
@admin_check
async def pin_message(c: Client, m: Message):
    if m.reply_to_message is None:
        return await m.reply_text(
            tl(m.chat.id, "reply_message_not_found"),
            quote=True
        )
    if len(m.command) > 1:
        state = m.text.split(" ", 1)
        if state == "silent":
            await m.reply_to_message.pin(disable_notification=True)
        else:
            await m.reply_to_message.pin(disable_notification=False)
    else:
        await m.reply_to_message.pin(disable_notification=False)
    await m.delete()


@Client.on_message(filters.command("unpin", prefixes=CONFIG.prefixes))
@admin_check
async def un_pin_message(c: Client, m: Message):
    if m.reply_to_message is None:
        return await m.reply_text(
            tl(m.chat.id, "reply_message_not_found"),
            quote=True
        )

    await m.reply_to_message.unpin()
    await m.reply_text(
        tl(m.chat.id, "successfully_unpinned"),
        quote=True
    )


@Client.on_message(filters.command("unpinall", prefixes=CONFIG.prefixes))
@admin_check
async def un_pinall_message(c: Client, m: Message):
    await c.unpin_all_chat_messages(m.chat.id)
    await m.reply_text(
        tl(m.chat.id, "successfully_unpinned_all"),
        quote=True
    )