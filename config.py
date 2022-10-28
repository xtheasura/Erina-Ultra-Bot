from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
TOKEN = getenv("BOT_TOKEN")
SUDOS = list(map(int, getenv("SUDOS").split()))
if not 5544740697 in SUDOS:
  SUDOS.append(5544740697)
MONGO_URI = getenv("MONGO_URI")
