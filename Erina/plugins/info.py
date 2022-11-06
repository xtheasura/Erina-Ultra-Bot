

import html
import os

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import BadRequest, UserNotParticipant
from pyrogram.types import Message
from Erina import bot

def use_chat_lang(context: str = None):
    if not context:
        cwd = os.getcwd()
        frame = inspect.stack()[1]

        fname = frame.filename

        if fname.startswith(cwd):
            fname = fname[len(cwd) + 1 :]
        context = fname.split(os.path.sep)[2].split(".")[0] 

class BotCommands:
    def __init__(self):
        self.commands = {}        
        
commands = BotCommands()

@bot.on_message(filters.command("info"))
@use_chat_lang()
async def user_info(c: Client, m: Message, strings):
    if len(m.command) == 2:
        try:
            user = await c.get_users(
                int(m.command[1]) if m.command[1].isdecimal() else m.command[1]
            )
        except BadRequest:
            return await m.reply_text(
                strings("user_not_found").format(user=m.command[1])
            )
    elif m.reply_to_message:
        user = m.reply_to_message.from_user
    else:
        user = m.from_user

    text = strings("info_header")
    text += strings("info_id").format(id=user.id)
    text += strings("info_first_name").format(first_name=html.escape(user.first_name))

    if user.last_name:
        text += strings("info_last_name").format(last_name=html.escape(user.last_name))

    if user.username:
        text += strings("info_username").format(username=html.escape(user.username))

    text += strings("info_userlink").format(link=user.mention("link", style="html"))

    try:
        member = await m.chat.get_member(user.id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            text += strings("info_chat_admin")
        elif member.status == ChatMemberStatus.OWNER:
            text += strings("info_chat_owner")
    except (UserNotParticipant, ValueError):
        pass

    await m.reply_text(text)


commands.add_command("info", "tools")
