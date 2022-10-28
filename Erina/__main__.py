from Erina import bot
import logging
from Erina.plugins import ALL_MODULES
from pyrogram import idle
import importlib
from pyrogram import filters
from Erina import BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
import asyncio

PM_ERINA_TEXT = """
**Sup!!! I Am Erina, Nice To Meet You!!**
I am And advanced Bot
**Report Issues - @**
"""

PM_ERINA_PIC = "https://telegra.ph/file/7107cb1bb3d4abc76b9c5.jpg"



START_KEYBOARD = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        text="Help",
        callback_data="bot_commands"
      ),
      InlineKeyboardButton(
        text="About Me",
        callback_data="abouterina"
      )
    ],
    [
      InlineKeyboardButton(
        text="Add To Your Group",
        url=f"https://t.me/{BOT_USERNAME}?startgroup=new"
      )
    ]
  ]
)

@bot.on_message(filters.command('start'))
async def miostart(_, message):
    return await message.reply_photo(
      photo=PM_ERINA_PIC,
      caption=PM_ERINA_TEXT,
      reply_markup=START_KEYBOARD
    ) 

FORMAT = "[INFO] %(message)s"

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
    )
    logging.getLogger("pyrogram").setLevel(logging.INFO)
    for module in ALL_MODULES:
      importlib.import_module("Mio.plugins." + module)
    
    print("I AM NOW ONLINE") 
    print("Project By Ryu120, Gift to my bich Tarun")
    idle()
