from pyrogram import Client, filters
from pyrogram.types import Message

from mia import CONFIG
from mia.modules.localization import tl
from mia.utils import admin_check


@Client.on_message(filters.command("purge", prefixes=CONFIG.prefixes))
@admin_check
async def purge_messages(c: Client, m: Message):
    chat = m.chat

    if m.reply_to_message:
        message_id = m.reply_to_message.message_id
        delete_to = m.message_id - 1
        if len(m.command) > 1:
            if (m.text.split(maxsplit=1)[1]).isdigit():
                new_delete = message_id + int(m.text.split(maxsplit=1)[1])
                if new_delete < delete_to:
                    delete_to = new_delete
        status_message = await m.reply_text(
            tl(chat.id, "starting_purge"),
            quote=True
        )

        count = 0

        for m_id in range(delete_to, message_id - 1, -1):
            await c.delete_messages(
                chat.id,
                m_id
            )

            count += 1
        await status_message.edit_text(
            tl(chat.id, "purge_success").format(count=count)
        )
    else:
        await m.reply_text(
            tl(chat.id, "reply_message_not_found"),
            quote=True
        )


@Client.on_message(filters.command("del", prefixes=CONFIG.prefixes))
@admin_check
async def delete_message(c: Client, m: Message):
    chat = m.chat

    if m.reply_to_message:
        message = m.reply_to_message
        await message.delete()
        await m.delete()
    else:
        await m.reply_text(
            tl(chat.id, "reply_message_not_found"),
            quote=True
        )
