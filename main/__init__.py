#ChauhanMahesh/Vasusen/DroneBots/COL

from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Basics
API_ID = 2992000
API_HASH = "235b12e862d71234ea222082052822fd"
BOT_TOKEN = "5225459357:AAEla1BFEr94OnHwKA9Ts05LLJS3Gpvqw-Y"
ACCESS_CHANNEL = int("-1001768362393")

Drone = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
