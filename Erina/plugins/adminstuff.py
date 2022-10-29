from pyrogram import filters
from Erina import bot, OWNER_ID as SUDOS, OWNER_ID2 as SUDO, BOT_ID
from Erina.utils.func import *
from time import time
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from Erina.utils.perms import *

async def extract_user(message, txr=None):
    return (await extract_user_and_reason(message, texr=txr))[0]

def parse_com(com, key):
  try:
    r = com.split(key,1)[1]
  except KeyError:
    return None
  r = (r.split(" ", 1)[1] if len(r.split()) >= 1 else None)
  return r

def user_mention(text):
  for i in text.split():
    if i.startswith("@"):
      return i[1:]


admins_in_chat = {}




async def list_admins(chat_id: int):
  global admins_in_chat
  if chat_id in admins_in_chat:
    interval = time() - admins_in_chat[chat_id]["last_updated_at"]
    if interval < 3600:
      return admins_in_chat[chat_id]["data"]
    else:
      members= await bot.get_chat_members(chat_id, filter="administrators")
      admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
          member.user.id for member in members
        ],
      }
  else:
    members= await bot.get_chat_members(chat_id, filter="administrators")
    admins_in_chat[chat_id] = {
      "last_updated_at": time(),
      "data": [
        member.user.id for member in members
      ],
    }

  return admins_in_chat[chat_id]["data"]



@bot.on_chat_member_updated()
async def admin_cache_func(_, cmu: ChatMemberUpdated):
  if cmu.old_chat_member and cmu.old_chat_member.promoted_by:
    members= await bot.get_chat_members(cmu.chat.id, filter="administrators")
    admins_in_chat[cmu.chat.id] = {
      "last_updated_at": time(),
      "data": [
        member.user.id for member in members
      ],
    }




@bot.on_message(filters.command("ban"))
@adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
  if not message.from_user.id in (await list_admins(message.chat.id) + SUDOS):
    return await message.reply_text("Become an admin first lol")
  user_id, reason = await extract_user_and_reason(message, sender_chat=True, texr=parse_com(message.text, "ban"))

  if not user_id:
    return await message.reply_text("`I Can't Find That User`")
  if user_id == BOT_ID:
    return await message.reply_text(
      "`I Can't Ban Myself, I Can Leave If You Want`"
    )
  if user_id in SUDOS:
    return await message.reply_text(
      "`Sorry Fella, That Guy's My Dev`"
    )
  if user_id in (await list_admins(message.chat.id)):
    return await message.reply_text(
      "`I Can't Ban A Fellow Admin`"
    )

  try:
    mention = (await bot.get_users(user_id)).mention
  except IndexError:
    mention = (
      message.reply_to_message.sender_chat.title
      if message.reply_to_message
      else "Anon"
    )

  msg = (
    f"**Banned User:** {mention}\n"
    f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
  )
  if reason:
    msg += f"**Reason:** `{reason}`"
  await message.chat.ban_member(user_id)
  await message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚠️ UNBAN", callback_data=f"unban_{user_id}")]]))
  
  
@bot.on_message(filters.command("tban"))
@adminsOnly("can_restrict_members")
async def tbanFunc(_, message: Message):
  if not message.from_user.id in (await list_admins(message.chat.id) + SUDOS):
    return await message.reply_text("Become an admin first lol")
  user_id, reason = await extract_user_and_reason(message, sender_chat=True, texr=parse_com(message.text, "tban"))

  if not user_id:
    return await message.reply_text("`I Can't Find That User`")
  if user_id == BOT_ID:
    return await message.reply_text(
      "`I Can't Ban Myself, I Can Leave If You Want`"
    )
  if user_id in SUDOS:
    return await message.reply_text(
      "`Sorry Fella, That Guy's My Dev`"
    )
  if user_id in (await list_admins(message.chat.id)):
    return await message.reply_text(
      "`I Can't Ban A Fellow Admin`"
    )

  try:
    mention = (await bot.get_users(user_id)).mention
  except IndexError:
    mention = (
      message.reply_to_message.sender_chat.title
      if message.reply_to_message
      else "Anon"
    )

  msg = (
    f"**Banned User:** {mention}\n"
    f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
  )  
  split = reason.split(None, 1)
  time_value = split[0]
  temp_reason = split[1] if len(split) > 1 else ""
  temp_ban = await time_converter(message, time_value)
  msg += f"**Banned For:** {time_value}\n"
  if temp_reason:
    msg += f"**Reason:** {temp_reason}"
  try:
    if len(time_value[:-1]) < 3:
      await message.chat.ban_member(user_id, until_date=temp_ban)
      await message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚠️ UNBAN", callback_data=f"unban_{user_id}")]]))
    else:
      await message.reply_text("`You Can't Use More Than 99`")
  except AttributeError:
    pass
  return




@bot.on_message(filters.command("dban"))
@adminsOnly("can_restrict_members")
async def dbanFunc(_, message: Message):
  if not message.from_user.id in (await list_admins(message.chat.id) + SUDOS):
    return await message.reply_text("Become an admin first lol")
  user_id, reason = await extract_user_and_reason(message, sender_chat=True, texr=parse_com(message.text, "dban"))

  if not user_id:
    return await message.reply_text("`I Can't Find That User`")
  if user_id == BOT_ID:
    return await message.reply_text(
      "`I Can't Ban Myself, I Can Leave If You Want`"
    )
  if user_id in SUDOS:
    return await message.reply_text(
      "`Sorry Fella, That Guy's My Dev`"
    )
  if user_id in (await list_admins(message.chat.id)):
    return await message.reply_text(
      "`I Can't Ban A Fellow Admin`"
    )

  try:
    mention = (await bot.get_users(user_id)).mention
  except IndexError:
    mention = (
      message.reply_to_message.sender_chat.title
      if message.reply_to_message
      else "Anon"
    )

  msg = (
    f"**Banned User:** {mention}\n"
    f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
  )
  if message.reply_to_message:
    await message.reply_to_message.delete()
  else:
    await message.delete()
  if reason:
    msg += f"**Reason:** `{reason}`"
  await message.chat.ban_member(user_id)
  await message.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚠️ UNBAN", callback_data=f"unban_{user_id}")]]))



@bot.on_message(filters.command("kick"))
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
  if not message.from_user.id in (await list_admins(message.chat.id) + SUDOS):
    return await message.reply_text("Become an admin first lol")
  user_id, reason = await extract_user_and_reason(message, sender_chat=True, texr=parse_com(message.text, "kick"))

  if not user_id:
    return await message.reply_text("`I Can't Find That User`")
  if user_id == BOT_ID:
    return await message.reply_text(
      "`I Can't Kick Myself, I Can Leave If You Want`"
    )
  if user_id in SUDOS:
    return await message.reply_text(
      "`Sorry Fella, That Guy's My Dev`"
    )
  if user_id in (await list_admins(message.chat.id)):
    return await message.reply_text(
      "`I Can't Kick A Fellow Admin`"
    )

  try:
    mention = (await bot.get_users(user_id)).mention
  except IndexError:
    mention = (
      message.reply_to_message.sender_chat.title
      if message.reply_to_message
      else "Anon"
    )

  msg = (
    f"**Kicked User:** {mention}\n"
    f"**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
  )
  if reason:
    msg += f"**Reason:** `{reason}`"
  await message.chat.ban_member(user_id)
  await message.chat.unban_member(user_id)
  await message.reply_text(msg)
  
  
@bot.on_message(filters.command("dkick"))
@adminsOnly("can_restrict_members")
async def dkickFunc(_, message: Message):
  if not message.from_user.id in (await list_admins(message.chat.id) + SUDOS):
    return await message.reply_text("Become an admin first lol")
  user_id, reason = await extract_user_and_reason(message, sender_chat=True, texr=parse_com(message.text, "dkick"))

  if not user_id:
    return await message.reply_text("`I Can't Find That User`")
  if user_id == BOT_ID:
    return await message.reply_text(
      "`I Can't Kick Myself, I Can Leave If You Want`"
    )
  if user_id in SUDOS:
    return await message.reply_text(
      "`Sorry Fella, That Guy's My Dev`"
    )
  if user_id in (await list_admins(message.chat.id)):
    return await message.reply_text(
      "`I Can't Kick A Fellow Admin`"
    )

  try:
    mention = (await bot.get_users(user_id)).mention
  except IndexError:
    mention = (
      message.reply_to_message.sender_chat.title
      if message.reply_to_message
      else "Anon"
    )

  msg = (
    f"**Kicked User:** {mention}\n"
    f"**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
  )
  if message.reply_to_message:
    await message.reply_to_message.delete()
  else:
    await message.delete()
  if reason:
    msg += f"**Reason:** `{reason}`"
  await message.chat.ban_member(user_id)
  await message.chat.unban_member(user_id)
  await message.reply_text(msg)


@bot.on_callback_query(filters.regex("^unban"))
async def _uban(_, query):
  if not query.from_user.id in (await list_admins(query.message.chat.id) or SUDOS):
    return await query.answer(text="You're Not An Admin Sun Of A Beech", show_alert=True)
  user_id = int(query.data.replace("unban_",""))
  await query.message.chat.unban_member(user_id)
  await query.message.edit_text(text=f"**Successfully Unbaned** {(await bot.get_users(user_id)).mention}")
  return await query.answer()

@bot.on_callback_query(filters.regex("^unmute"))
async def _umute(_, query):
  if not query.from_user.id in (await list_admins(query.message.chat.id) or SUDOS):
    return await query.answer(text="You're Not An Admin Sun Of A Beech", show_alert=True)
  user_id = int(query.data.replace("unmute_",""))
  await query.message.edit_text(text=f"**Successfully Unmuted** {(await bot.get_users(user_id)).mention}")
  return await query.answer()




@bot.on_message(filters.command("unban") & ~filters.edited & ~filters.private)
@adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    reply = message.reply_to_message

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("You cannot unban a channel")

    if len(message.command) == 2:
        user = parse_com(message.text, "unban")
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await bot.get_users(user)).mention
    await message.reply_text(f"Unbanned! {umention}")



@bot.on_message(filters.command("del") & ~filters.edited & ~filters.private)
@adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message To Delete It")
    await message.reply_to_message.delete()
    await message.delete()


@bot.on_message(
    filters.command("fullpromote")
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message, txr=parse_com(message.text, "fullpromote"))
    umention = (await bot.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text("I can't find that user.")
    app = await bot.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not app.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=app.can_change_info,
        can_invite_users=app.can_invite_users,
        can_delete_messages=app.can_delete_messages,
        can_restrict_members=app.can_restrict_members,
        can_pin_messages=app.can_pin_messages,
        can_promote_members=app.can_promote_members,
        can_manage_chat=app.can_manage_chat,
        can_manage_voice_chats=app.can_manage_voice_chats,
    )
    return await message.reply_text(f"Fully Promoted! {umention}")



@bot.on_message(
    filters.command("promote")
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message, txr=parse_com(message.text, "promote"))
    umention = (await bot.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text("I can't find that user.")
    app = await bot.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not app.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=app.can_invite_users,
        can_delete_messages=app.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=app.can_manage_chat,
        can_manage_voice_chats=app.can_manage_voice_chats,
    )
    await message.reply_text(f"Promoted! {umention}")



@bot.on_message(
    filters.command(["pin", "unpin"]) & ~filters.edited & ~filters.private
)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin/unpin it.")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )



@bot.on_message(
    filters.command("tmute") & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, texr=parse_com(message.text, "tmute"))
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOS:
        return await message.reply_text(
            "Sorry Fella, That Guy's My Dev!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't mute an admin, You know the rules, so do i."
        )
    mention = (await bot.get_users(user_id)).mention
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="🚨   Unmute   🚨", callback_data=f"unmute_{user_id}")]])
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    split = reason.split(None, 1)
    time_value = split[0]
    temp_reason = split[1] if len(split) > 1 else ""
    temp_mute = await time_converter(message, time_value)
    msg += f"**Muted For:** {time_value}\n"
    if temp_reason:
        msg += f"**Reason:** {temp_reason}"
    try:
        if len(time_value[:-1]) < 3:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=temp_mute,
            )
            await message.reply_text(msg, reply_markup=keyboard)
        else:
            await message.reply_text("You can't use more than 99")
    except AttributeError:
        pass
    return



@bot.on_message(
    filters.command("mute") & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, texr=parse_com(message.text, "mute"))
    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == BOT_ID:
        return await message.reply_text("I can't mute myself.")
    if user_id in SUDOS:
        return await message.reply_text(
            "Sorry Fella, That Guy's My Dev!"
        )
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(
            "I can't mute an admin, You know the rules, so do i."
        )
    mention = (await bot.get_users(user_id)).mention
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="🚨   Unmute   🚨", callback_data=f"unmute_{user_id}")]])
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await message.reply_text(msg, reply_markup=keyboard)
