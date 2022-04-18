import io
import re

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from mia import CONFIG
from mia.database.filters import add_filter, get_all_filters, count_filters, delete_filter, delete_all_filters, find_filter_one
from mia.database.notes import find_one_note
from mia.database.welcome import get_welcome
from mia.modules.localization import tl
from mia.utils import split_quotes, admin_check, button_markdown_parser, check_for_filters, chat_owner_only


@Client.on_message(filters.command(["addfilter", "filter", "savefilter"], prefixes=CONFIG.prefixes))
@admin_check
async def add_filter_command(c: Client, m: Message):
    chat = m.chat
    args = m.text.markdown.split(maxsplit=1)
    split_text = split_quotes(args[1])
    trigger = split_text[0].lower()
    if m.reply_to_message is None and len(split_text) < 2:
        await m.reply_text(tl(chat.id, "filter_content_empty"), quote=True)
        return

    if m.reply_to_message and m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
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
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
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
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
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
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
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
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
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
        raw_data = split_text[1] if len(split_text) > 1 else None
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
        msg = await c.send_sticker(
            chat_id=CONFIG.filter_dump_chat,
            sticker=file_id,
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    else:
        raw_data = split_text[1]
        data, button, alerts = button_markdown_parser(raw_data, trigger, "filter")
        msg = await c.send_message(
            chat_id=CONFIG.filter_dump_chat,
            text=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )

    add_filter(str(chat.id), trigger, str(msg.message_id), alerts)
    await m.reply_text(
        tl(chat.id, "successfully_added_filter").format(trigger=trigger, chat_name=chat.title),
        quote=True
    )


@Client.on_message(filters.command(["filters", "viewfilters"], prefixes=CONFIG.prefixes))
@admin_check
async def get_all_filters_command(c: Client, m: Message):
    chat = m.chat
    trigger_list = [x.trigger for x in get_all_filters(str(chat.id))]
    count_triggers = count_filters(str(chat.id))
    if count_triggers > 0:
        filter_list_text = tl(chat.id, "all_filters_text").format(
            chat_name=chat.title,
            count=count_triggers
        )

        for triggers in trigger_list:
            filter_list_text += f" - `{triggers}`\n"

        if len(filter_list_text) > 4096:
            with io.BytesIO(str.encode(filter_list_text.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await m.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filter_list_text = tl(chat.id, "no_filter_found").format(
            chat_name=chat.title)

    await m.reply_text(
        text=filter_list_text,
        quote=True,
        parse_mode="md"
    )


@Client.on_message(filters.command(["delfilter"], prefixes=CONFIG.prefixes))
@admin_check
async def del_filter_command(c: Client, m: Message):
    chat = m.chat

    if len(m.command) < 2:
        return await m.reply_text(
            tl(chat.id, "del_filter_args_not_found")
        )
    args = m.text.split(maxsplit=1)
    trigger = args[1].lower()
    check = check_for_filters(str(chat.id), trigger)
    if check:
        text = tl(chat.id, "successfully_deleted_filter").format(filter=trigger)
        delete_filter(str(chat.id), trigger)
    else:
        text = tl(chat.id, "no_filter_found")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(filters.command(["delall"], prefixes=CONFIG.prefixes))
@chat_owner_only
async def del_all_filter_command(c: Client, m: Message):
    chat = m.chat
    count_triggers = count_filters(str(chat.id))
    if count_triggers > 0:
        text = tl(chat.id, "deleted_all_filters").format(count=count_triggers)
        delete_all_filters(str(chat.id))
    else:
        text = tl(chat.id, "no_filter_found")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(
    (filters.group | filters.private) & filters.text & filters.incoming, group=1
)
async def serve_filter(c: Client, m: Message):
    chat_id = m.chat.id
    text = m.text
    targeted_message = m.reply_to_message or m

    if m.text.startswith(tuple(CONFIG.prefixes)):
        return None

    all_filters = get_all_filters(str(chat_id))
    for filter_s in all_filters:
        keyword = filter_s.trigger
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            data = await c.get_messages(
                CONFIG.filter_dump_chat,
                int(filter_s.message_id)
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


@Client.on_callback_query(filters.regex("^alert:.*"))
async def alert_message(c: Client, m: CallbackQuery):
    chat = m.message.chat
    query = m.data.split(":", 4)
    alerts = None
    if query[1] == "filter":
        alerts = find_filter_one(str(chat.id), query[3])
    elif query[1] == "note":
        alerts = find_one_note(str(chat.id), query[3])
    elif query[1] == "greeting":
        alerts = get_welcome(str(chat.id))
    if alerts is not None:
        alert = alerts.alerts[int(query[2])]
        alert = alert.replace("\\n", "\n").replace("\\t", "\t")
        await m.answer(alert, show_alert=True)
