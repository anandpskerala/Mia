import re
import time
from typing import List
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    Chat
)

from mia import CONFIG


# NOTE: the url \ escape may cause double escapes
# match * (bold) (don't escape if in url)
# match _ (italics) (don't escape if in url)
# match ` (code)
# match []() (markdown link)
# else, escape *, _, `, and [
from mia.database.filters import get_all_filters
from mia.database.notes import get_all_notes

MATCH_MD = re.compile(r'\*(.*?)\*|'
                      r'_(.*?)_|'
                      r'`(.*?)`|'
                      r'(?<!\\)(\[.*?\])(\(.*?\))|'
                      r'(?P<esc>[*_`\[])')

# regex to find []() links -> hyperlinks/buttons
LINK_REGEX = re.compile(r'(?<!\\)\[.+?\]\((.*?)\)')
BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\((buttonurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))"
)

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)


DEFAULT_WELCOME_MESSAGES = [
    "{first_name} is here!",
    "Ready player {first_name}",
    "Genos, {first_name} is here.",
    "A wild {first_name} appeared.",
    "{first_name} came in like a Lion!",
    "{first_name} has joined your party.",
    "{first_name} just joined. Can I get a heal?",
    "{first_name} just joined the chat - asdgfhak!",
    "{first_name} just joined. Everyone, look busy!",
    "Welcome, {first_name}. Stay awhile and listen.",
    "Welcome, {first_name}. We were expecting you ( ͡° ͜ʖ ͡°)",
    "Welcome, {first_name}. We hope you brought pizza.",
    "Welcome, {first_name}. Leave your weapons by the door.",
    "Swoooosh. {first_name} just landed.",
    "Brace yourselves. {first_name} just joined the chat.",
    "{first_name} just joined. Hide your bananas.",
    "{first_name} just arrived. Seems OP - please nerf.",
    "{first_name} just slid into the chat.",
    "A {first_name} has spawned in the chat.",
    "Big {first_name} showed up!",
    "Where’s {first_name}? In the chat!",
    "{first_name} hopped into the chat. Kangaroo!!",
    "{first_name} just showed up. Hold my beer.",
    "Challenger approaching! {first_name} has appeared!",
    "It's a bird! It's a plane! Nevermind, it's just {first_name}.",
    "It's {first_name}! Praise the sun! \o/",
    "Never gonna give {first_name} up. Never gonna let {first_name} down.",
    "Ha! {first_name} has joined! You activated my trap card!",
    "Cheers, love! {first_name}'s here!",
    "Hey! Listen! {first_name} has joined!",
    "We've been expecting you {first_name}",
    "It's dangerous to go alone, take {first_name}!",
    "{first_name} has joined the chat! It's super effective!",
    "Cheers, love! {first_name} is here!",
    "{first_name} is here, as the prophecy foretold.",
    "{first_name} has arrived. Party's over.",
    "{first_name} is here to kick butt and chew bubblegum. And {first_name} is all out of gum.",
    "Hello. Is it {first_name} you're looking for?",
    "{first_name} has joined. Stay a while and listen!",
]


def button_markdown_parser(msg: str, keyword: str, typo: str):
    text = msg
    buttons = []
    note_data = ""
    alerts = []
    if text is None:
        return note_data, buttons, None
        #
    if text.startswith(tuple(CONFIG.prefixes)):
        args = text.split(None, 2)
        # use python's maxsplit to separate cmd and args
        text = args[2]

    prev = 0
    i = 0
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev:match.start(1)]
            prev = match.end(1)
            if match.group(3) == "buttonalert":
                # create a thruple with button label, url, and newline status
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alert:{typo}:{i}:{keyword}"
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alert:{typo}:{i}:{keyword}"
                    )])
                i = i + 1
                alerts.append(match.group(4))
            else:
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        url=match.group(4).replace(" ", "")
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        url=match.group(4).replace(" ", "")
                    )])

        # if odd, escaped -> move along
        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]
    return note_data, buttons, alerts if len(alerts) != 0 else None


def format_welcome_caption(md_string, chat_member, chat: Chat):
    return md_string.format(
        dc_id=chat_member.dc_id,
        first_name=chat_member.first_name,
        id=chat_member.id,
        last_name=chat_member.last_name or chat_member.first_name,
        mention=chat_member.mention,
        username=chat_member.username,
        chatname=chat.title,
        fullname=f'{chat_member.first_name} {chat_member.last_name}',
        count=chat.members_count
    )


def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res


def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (
                text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
            ):
                break
            counter += 1
        else:
            return text.split(None, 1)

        key = remove_escapes(text[1:counter].strip())
        rest = text[counter + 1:].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    return text.split(None, 1)


def check_for_filters(chat_id: str, trigger: str):
    all_filters = get_all_filters(chat_id)
    for keywords in all_filters:
        keyword = keywords.trigger
        if trigger == keyword:
            return True
    return False


def check_for_notes(chat_id: str, trigger: str):
    all_notes = get_all_notes(chat_id)
    for keywords in all_notes:
        keyword = keywords.trigger
        if trigger == keyword:
            return True
    return False


def get_file_id(msg):
    content = None
    if msg.media:
        if msg.sticker:
            content = msg.sticker.file_id

        elif msg.document:
            content = msg.document.file_id

        elif msg.photo:
            content = msg.photo.file_id

        elif msg.audio:
            content = msg.audio.file_id

        elif msg.voice:
            content = msg.voice.file_id

        elif msg.video:
            content = msg.video.file_id

        elif msg.video_note:
            content = msg.video_note.file_id

    return content
