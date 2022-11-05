import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
TOKEN = getenv("BOT_TOKEN")
MONGO_URI = getenv("MONGO_URI")
OWNER_ID = int(os.environ.get("OWNER_ID", "7351948"))
OWNER_ID2 = int(os.environ.get("OWNER_ID", "7351948"))
