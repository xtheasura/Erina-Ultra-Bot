from pyrogram import filters , Client
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from typing import Union
import os 
import time
from Erina.fonts import FONTS
from config import *

bot = Client(
    'Erina',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

print("[INFO]: INITIALIZING DATABASE")
async_mongo_client = async_mongo(MONGO_URI)
db = async_mongo_client.mio


START_TIME = time.time()
bot.start()
x = bot.get_me()
BOT_USERNAME = x.username
BOT_NAME = x.first_name
BOT_ID = x.id 

x = None


MOD_LOAD = []
MOD_NOLOAD = []
