from pyrogram import filters
from Erina import bot
from Erina.helper_functions.extract_user import extract_user
from Erina.helper_functions.cust_p_filters import admin_fliter
from datetime import datetime, timedelta
import time
from pyrogram.types import ChatPermissions

def extract_time(time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            return None

        if unit == "s":
            bantime = datetime.now() + timedelta(seconds=int(time_num))
        elif unit == "m":
            bantime = datetime.now() + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = datetime.now() + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = datetime.now() + timedelta(days=int(time_num))
        else:
            # how even...?
            return None
        return bantime
    else:
        return None


def format_welcome_caption(html_string, chat_member):
    return html_string.format(
        dc_id=chat_member.dc_id,
        first_name=chat_member.first_name,
        id=chat_member.id,
        last_name=chat_member.last_name,
        mention=chat_member.mention,
        username=chat_member.username,
    )

@bot.on_message(filters.command("ban") & admin_fliter)
async def ban_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "I see..! "
                f"{user_first_name}"
                " Banned This Bakaaa!."
            )
        else: 
            await message.reply_text(
                "I see..! "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " Banned This Bakaaa!."
            )


@bot.on_message(filters.command("tban") & admin_fliter)
async def temp_ban_user(_, message):
    if not len(message.command) > 1:
        return

    user_id, user_first_name, _ = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Not Valid. "
                "Expected value m, h, or d, Is Not Valid: {}"
            ).format(message.command[1][-1])
        )
        return

    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "I see..! "
                f"{user_first_name}"
                f" banned for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "I see..! "
                f"<a href='tg://user?id={user_id}'>"
                "Baka"
                "</a>"
                f" banned for {message.command[1]}!"
            )

@bot.on_message(
    filters.command(["unban", "unmute"]) & admin_fliter
)
async def un_ban_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Okay Unbanned This Baka "
                f"{user_first_name} baka "
                " Can Join Again!"
            )
        else:
            await message.reply_text(
                "Okay Unbanned This Baka "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> baka "
                " Can Join Again!"
            )                        



@bot.on_message(filters.command("mute") & admin_fliter)
async def mute_user(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id, permissions=ChatPermissions()
        )
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "On it🏻 " f"{user_first_name}" " Muted this baka"
            )
        else:
            await message.reply_text(
                "On it🏻 "
                f"<a href='tg://user?id={user_id}'>"
                "Bakkaaa"
                "</a>"
                " Muted This Baka"
            )


@bot.on_message(filters.command("tmute") & admin_fliter)
async def temp_mute_user(_, message):
    if not len(message.command) > 1:
        return

    user_id, user_first_name, _ = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Not Valid. "
                "Expected value m, h, or d, Value u gave: {}"
            ).format(message.command[1][-1])
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id, permissions=ChatPermissions(), until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Yeah Shut up for a while!"
                f"{user_first_name}"
                f" muted for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Yeah Shut up for a while!"
                f"<a href='tg://user?id={user_id}'>"
                "Baka"
                "</a>"
                " bakaaaa "
                f" muted for {message.command[1]}!"
            )            
            
__MODULE__ = "Admin"
__HELP__ = """/ban - Ban A User
/unban - To unban a user
/tban - Ban A User For Specific Time"""            
