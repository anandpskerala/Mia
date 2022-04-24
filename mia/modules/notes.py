import io

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from mia import CONFIG
from mia.database.notes import add_note, get_all_notes, count_notes, delete_note, delete_all_notes, find_one_note
from mia.modules.localization import tl
from mia.utils import admin_check, button_markdown_parser, check_for_notes, chat_owner_only


@Client.on_message(filters.command(["addnote", "note", "savenote"], prefixes=CONFIG.prefixes))
@admin_check
async def add_note_command(c: Client, m: Message):
    chat = m.chat
    args = m.text.markdown.split(maxsplit=2)
    if m.reply_to_message is None and len(args) < 3:
        await m.reply_text(tl(chat.id, "note_content_empty"), quote=True)
        return

    trigger = args[1].lower()

    if m.reply_to_message and m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_photo(
            chat_id=CONFIG.filter_dump_chat,
            photo=file_id,
            caption=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    elif m.reply_to_message and m.reply_to_message.document:
        file_id = m.reply_to_message.document.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_document(
            chat_id=CONFIG.filter_dump_chat,
            document=file_id,
            caption=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )

    elif m.reply_to_message and m.reply_to_message.video:
        file_id = m.reply_to_message.video.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_video(
            chat_id=CONFIG.filter_dump_chat,
            video=file_id,
            caption=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )

    elif m.reply_to_message and m.reply_to_message.audio:
        file_id = m.reply_to_message.audio.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_audio(
            chat_id=CONFIG.filter_dump_chat,
            audio=file_id,
            caption=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    elif m.reply_to_message and m.reply_to_message.animation:
        file_id = m.reply_to_message.animation.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_animation(
            chat_id=CONFIG.filter_dump_chat,
            animation=file_id,
            caption=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    elif m.reply_to_message and m.reply_to_message.sticker:
        file_id = m.reply_to_message.sticker.file_id
        raw_data = args[2] if len(args) > 2 else None
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_sticker(
            chat_id=CONFIG.filter_dump_chat,
            sticker=file_id,
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    else:
        raw_data = args[2]
        data, button, alerts = button_markdown_parser(raw_data, trigger, "note")
        msg = await c.send_message(
            chat_id=CONFIG.filter_dump_chat,
            text=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )

    add_note(str(chat.id), trigger, str(msg.message_id), alerts)
    await m.reply_text(
        tl(chat.id, "successfully_added_note").format(trigger=trigger, chat_name=chat.title),
        quote=True
    )


@Client.on_message(filters.command(["notes", "viewnotes"], prefixes=CONFIG.prefixes))
@admin_check
async def get_all_notes_command(c: Client, m: Message):
    chat = m.chat
    trigger_list = [x.trigger for x in get_all_notes(str(chat.id))]
    count_triggers = count_notes(str(chat.id))
    if count_triggers > 0:
        note_list_text = tl(chat.id, "all_notes_text").format(
            chat_name=chat.title,
            count=count_triggers
        )

        for triggers in trigger_list:
            note_list_text += f" - `{triggers}`\n"

        if len(note_list_text) > 4096:
            with io.BytesIO(str.encode(note_list_text.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await m.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        note_list_text = tl(chat.id, "no_note_found").format(
            chat_name=chat.title)

    await m.reply_text(
        text=note_list_text,
        quote=True,
        parse_mode="md"
    )


@Client.on_message(filters.command(["delnote"], prefixes=CONFIG.prefixes))
@admin_check
async def del_note_command(c: Client, m: Message):
    chat = m.chat

    if len(m.command) < 2:
        return await m.reply_text(
            tl(chat.id, "del_note_args_not_found")
        )
    args = m.text.split(maxsplit=1)
    trigger = args[1].lower()
    check = check_for_notes(str(chat.id), trigger)
    if check:
        text = tl(chat.id, "successfully_deleted_note").format(note=trigger)
        delete_note(str(chat.id), trigger)
    else:
        text = tl(chat.id, "no_note_found")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(filters.command(["rmall"], prefixes=CONFIG.prefixes))
@chat_owner_only
async def del_all_note_command(c: Client, m: Message):
    chat = m.chat
    count_triggers = count_notes(str(chat.id))
    if count_triggers > 0:
        text = tl(chat.id, "deleted_all_notes").format(count=count_triggers)
        delete_all_notes(str(chat.id))
    else:
        text = tl(chat.id, "no_note_found")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(
    (filters.group | filters.private) & filters.regex("^#[^\s]+") & filters.incoming
)
async def serve_notes(c: Client, m: Message):
    chat_id = m.chat.id
    text = m.text
    targeted_message = m.reply_to_message or m

    f_word = text.split()[0]
    no_hash = f_word[1:]
    note = find_one_note(str(chat_id), no_hash)
    if note:
        data = await c.get_messages(
            CONFIG.filter_dump_chat,
            int(note.message_id)
        )
        if data.text:
            await targeted_message.reply_text(
                data.text,
                quote=True,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.photo:
            await targeted_message.reply_photo(
                data.photo.file_id,
                quote=True,
                caption=data.caption,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.document:
            await targeted_message.reply_document(
                data.document.file_id,
                quote=True,
                caption=data.caption,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.video:
            await targeted_message.reply_video(
                data.video.file_id,
                quote=True,
                caption=data.caption,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.audio:
            await targeted_message.reply_audio(
                data.audio.file_id,
                quote=True,
                caption=data.caption,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.animation:
            await targeted_message.reply_animation(
                data.animation.file_id,
                quote=True,
                caption=data.caption,
                parse_mode="md",
                reply_markup=data.reply_markup
            )
        elif data.sticker:
            await targeted_message.reply_sticker(
                data.sticker.file_id,
                quote=True,
                reply_markup=data.reply_markup
            )

