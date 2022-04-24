from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from mia import CONFIG
from mia.modules.localization import tl
from mia.utils import admin_check, get_user_and_text
from mia.database.warns import add_user_warn, get_warn_settings, remove_last_warn


@Client.on_message(filters.command("warn", prefixes=CONFIG.prefixes) & filters.group)
@admin_check
async def warn_user_command(c: Client, m: Message):
    chat = m.chat
    user, reason = await get_user_and_text(c, m)
    if user:
        num_warns = add_user_warn(str(chat.id), str(user.id), reason)
        warn_settings = get_warn_settings(str(chat.id))
        if not warn_settings:
            warn_limit = 3
        else:
            warn_limit = int(warn_settings.limit)

        text = tl(chat.id, "warn_user_text").format(
            mention=user.mention,
            num_warns=num_warns,
            warn_limit=warn_limit
        )
        keyboard = [
            [
                InlineKeyboardButton(tl(chat.id, "remove_warn_button"), callback_data=f"rm_warn_{user.id}")
            ]
        ]
        if reason:
            text += tl(chat.id, "warn_user_text_reason").format(reason=reason)
        await m.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        if int(num_warns) == warn_limit:
            await chat.ban_member(user.id)


@Client.on_callback_query(filters.regex("^rm_warn_.*"))
async def remove_warn_button(c: Client, m: CallbackQuery):
    chat = m.message.chat
    user_id = m.data.split("_", 2)[2]
    remove_last_warn(str(chat.id), user_id)
    user = await c.get_users(user_id)
    text = tl(chat.id, "warning_removed").format(
        admin=m.from_user.mention,
        user=user.mention
    )
    await m.edit_message_text(text)
