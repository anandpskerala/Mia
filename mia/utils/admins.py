from functools import wraps, partial
from typing import Union

from pyrogram import Client
from pyrogram.types import Chat, Message, CallbackQuery

from mia import CONFIG
from mia.modules.localization import tl


async def is_bot_admin(chat: Chat, bot: Client):
    bot_id = (await bot.get_me()).id
    chat_member = await chat.get_member(bot_id)
    if chat_member.status in ['administrator', 'creator']:
        return True
    return False


async def is_user_admin(chat: Chat, user_id: int):
    chat_member = await chat.get_member(user_id)
    if chat_member.status in ['administrator', 'creator']:
        return True
    elif chat_member.is_anonymous:
        return True
    else:
        return False


def admin_check(func):
    @wraps(func)
    async def wrapper(c: Client, m: Union[Message, CallbackQuery], *args, **kwargs):
        if isinstance(m, CallbackQuery):
            msg = m.message
            chat = msg.chat
            user = msg.from_user
            method = m.answer
        else:
            msg = m
            chat = m.chat
            user = msg.from_user
            method = m.reply_text
        if chat.type == "private":
            return await func(c, m, *args, **kwargs)

        if await is_bot_admin(chat, c):
            if await is_user_admin(chat, user.id):
                return await func(c, m, *args, **kwargs)
            else:
                return await method(tl(chat.id, "user_not_admin"))
        else:
            return await method(tl(chat.id, "bot_not_admin"))
    return wrapper
