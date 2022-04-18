import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from mia import CONFIG
from mia.modules.localization import tl
from mia.utils import admin_check, button_markdown_parser, get_file_id, format_welcome_caption,\
    DEFAULT_WELCOME_MESSAGES
from mia.database.welcome import add_welcome_strings, get_welcome, set_previous_welcome, set_welcome_state,\
    set_clean_welcome, set_clean_service, reset_welcome


@Client.on_message(filters.command(["addwelcome", "setwelcome"], prefixes=CONFIG.prefixes))
@admin_check
async def add_welcome(c: Client, m: Message):
    chat = m.chat
    args = m.text.markdown.split(maxsplit=1)
    if m.reply_to_message is None and len(args) < 2:
        await m.reply_text(tl(chat.id, "welcome_content_empty"), quote=True)
        return

    if m.reply_to_message and m.reply_to_message.photo:
        file_id = m.reply_to_message.photo.file_id
        raw_data = (
            m.reply_to_message.caption.markdown
            if m.reply_to_message.caption is not None
            else None
        )
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
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
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
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
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
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
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
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
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
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
        raw_data = args[1] if len(args) > 1 else None
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
        msg = await c.send_sticker(
            chat_id=CONFIG.filter_dump_chat,
            sticker=file_id,
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )
    else:
        raw_data = args[1]
        data, button, alerts = button_markdown_parser(raw_data, "+", "greeting")
        msg = await c.send_message(
            chat_id=CONFIG.filter_dump_chat,
            text=data,
            parse_mode="md",
            reply_markup=InlineKeyboardMarkup(button)
            if len(button) != 0
            else None,
        )

    if m.reply_to_message and m.media:
        no_format = await c.send_cached_media(
            CONFIG.filter_dump_chat,
            file_id=get_file_id(m.reply_to_message),
            caption=m.caption,
            parse_mode=None
        )
    else:
        no_format = await c.send_message(CONFIG.filter_dump_chat, args[1], parse_mode=None)
    add_welcome_strings(str(chat.id), str(msg.message_id), alerts, True, str(no_format.message_id))
    await m.reply_text(
        tl(chat.id, "successfully_added_welcome").format(chat_name=chat.title),
        quote=True
    )


@Client.on_message(filters.new_chat_members)
async def serve_welcome(c: Client, m: Message):
    chat = m.chat
    chat_id = m.chat.id
    members = await c.get_chat_members_count(chat_id)
    chat.members_count = members
    welcome = get_welcome(str(chat_id))
    if welcome and welcome.state:
        msg_id = welcome.message_id
        note_msg = await c.get_messages(CONFIG.filter_dump_chat, int(msg_id))
        for n_m in m.new_chat_members:
            if note_msg.media:
                file_id = get_file_id(note_msg)
                current_msg = await m.reply_cached_media(
                    file_id=file_id,
                    caption=format_welcome_caption(note_msg.caption.markdown, n_m, chat),
                    parse_mode="md",
                    reply_markup=note_msg.reply_markup
                )
            else:
                current_msg = await m.reply_text(
                    text=format_welcome_caption(note_msg.text.markdown, n_m, chat),
                    parse_mode="md",
                    reply_markup=note_msg.reply_markup
                )

            if welcome.clean_service:
                await m.delete()

            if welcome.clean_welcome:
                await c.delete_messages(
                    chat_id,
                    int(welcome.previous_welcome)
                )
            set_previous_welcome(str(chat_id), str(current_msg.message_id))
    else:
        for n_m in m.new_chat_members:
            await m.reply_text(
                format_welcome_caption(random.choice(DEFAULT_WELCOME_MESSAGES), n_m, chat)
            )


@Client.on_message(filters.command(["welcome", "viewwelcome"], prefixes=CONFIG.prefixes))
@admin_check
async def check_welcome(c: Client, m: Message):
    chat = m.chat
    if len(m.command) > 1:
        args = m.text.split(maxsplit=1)
    else:
        args = None

    chat_id = chat.id
    welcome = get_welcome(str(chat_id))

    text = tl(chat_id, "welcome_settings").format(
        state=welcome.state if welcome else False,
        clean_welcome=welcome.clean_welcome if welcome else False,
        clean_service=welcome.clean_service if welcome else False
    )

    if args:
        if args[1] in ["on", "yes"]:
            set_welcome_state(str(chat.id), True)
            text = tl(chat_id, "set_welcome_state").format(args=args[1])
            await m.reply_text(
                text,
                quote=True,
                parse_mode="md"
            )
        elif args[1] in ["off", "no"]:
            set_welcome_state(str(chat.id), False)
            text = tl(chat_id, "set_welcome_state").format(args=args[1])
            await m.reply_text(
                text,
                quote=True,
                parse_mode="md"
            )
        elif args[1] == "noformat":
            if welcome:
                await m.reply_text(
                    text,
                    quote=True,
                    parse_mode="md"
                )
                note_msg = await c.get_messages(CONFIG.filter_dump_chat, int(welcome.no_format))
                if note_msg.media:
                    file_id = get_file_id(note_msg)
                    await m.reply_cached_media(
                        file_id=file_id,
                        caption=note_msg.caption.markdown,
                        parse_mode=None
                    )
                else:
                    await m.reply_text(
                        text=note_msg.text.markdown,
                        parse_mode=None
                    )
        else:
            await m.reply_text(
                text=tl(chat_id, "wrong_arg_found"),
                quote=True
            )

    else:
        if welcome:
            await m.reply_text(
                text,
                quote=True,
                parse_mode="md"
            )
            note_msg = await c.get_messages(CONFIG.filter_dump_chat, int(welcome.message_id))
            if note_msg.media:
                file_id = get_file_id(note_msg)
                await m.reply_cached_media(
                    file_id=file_id,
                    caption=note_msg.caption.markdown,
                    parse_mode="md",
                    reply_markup=note_msg.reply_markup
                )
            else:
                await m.reply_text(
                    text=note_msg.text.markdown,
                    parse_mode="md",
                    reply_markup=note_msg.reply_markup
                )
        else:
            await m.reply_text(
                random.choice(DEFAULT_WELCOME_MESSAGES),
                quote=True
            )


@Client.on_message(filters.command(["cleanwelcome", "set_cleanwelcome"], prefixes=CONFIG.prefixes))
@admin_check
async def clean_welcomes(c: Client, m: Message):
    chat = m.chat
    chat_id = chat.id
    if len(m.command) > 1:
        args = m.text.split(maxsplit=1)
    else:
        args = None

    if args:
        if args[1].lower() in ['on', 'yes']:
            set_clean_welcome(str(chat_id), True)
            text = tl(chat_id, "set_clean_welcome").format(args="on")
        elif args[1].lower() in ['off', 'no']:
            set_clean_welcome(str(chat_id), False)
            text = tl(chat_id, "set_clean_welcome").format(args="off")
        else:
            text = tl(chat_id, "wrong_arg_found")
    else:
        welcome = get_welcome(str(chat_id))
        if welcome and welcome.clean_welcome:
            text = tl(chat_id, "clean_welcome_on")
        else:
            text = tl(chat_id, "clean_welcome_off")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(filters.command(["cleanservice", "set_cleanservice"], prefixes=CONFIG.prefixes))
@admin_check
async def clean_service(c: Client, m: Message):
    chat = m.chat
    chat_id = chat.id
    if len(m.command) > 1:
        args = m.text.split(maxsplit=1)
    else:
        args = None

    if args:
        if args[1].lower() in ['on', 'yes']:
            set_clean_service(str(chat_id), True)
            text = tl(chat_id, "set_clean_service").format(args="on")
        elif args[1].lower() in ['off', 'no']:
            set_clean_service(str(chat_id), False)
            text = tl(chat_id, "set_clean_service").format(args="off")
        else:
            text = tl(chat_id, "wrong_arg_found")
    else:
        welcome = get_welcome(str(chat_id))
        if welcome and welcome.clean_service:
            text = tl(chat_id, "clean_service_on")
        else:
            text = tl(chat_id, "clean_service_off")
    await m.reply_text(
        text,
        quote=True
    )


@Client.on_message(filters.command("resetwelcome", prefixes=CONFIG.prefixes))
@admin_check
async def reset_welcome_settings(c: Client, m: Message):
    chat = m.chat
    chat_id = chat.id
    reset_welcome(str(chat_id))
    await m.reply_text(
        tl(chat_id, "reset_welcome"),
        quote=True
    )
