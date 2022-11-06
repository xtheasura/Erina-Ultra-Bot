from pyrogram import filters

from Erina import bot


@bot.on_message(filters.command("alive"))
async def alive(bot, message):
    await message.reply_text("`I'm alive` \n PTB: `v20.a0` \n Pyrogram: `2.0.57`")
