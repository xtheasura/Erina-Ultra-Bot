from Bot import bot
from pyrogram import filters


@bot.on_message(filters.command("info"))
def info(bot, message):
  user = message.from_user.id
    
  
  dta = bot.get_users(user)
  data = f"""**|-First Name** : {dta.first_name}
**|-Last Name**: {dta.last_name}
**|-Telegram Id**: {dta.id}
**|-PermaLink**: {dta.mention(message.from_user.first_name)}
"""
  message.reply_text(data)
  

  
  
@bot.on_message(filters.command('id'))
def ids(_,message):
  reply = message.reply_to_message
  if reply:
    message.reply_text(f"**Your ID**: `{message.from_user.id}`\n**{reply.from_user.first_name}'s ID**: `{reply.from_user.id}`")
  else:
    message.reply(f"**chat id**: `{message.chat.id}`")
