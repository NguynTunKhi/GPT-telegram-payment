import yaml
from pathlib import Path

with open("locales/en.yml", 'r') as f:
    locales_yaml = yaml.safe_load(f)

with open("locales/modes.yml", 'r') as f:
    chat_modes = yaml.safe_load(f)

bot_token = locales_yaml["settings"]["bot_token"]
api_id = locales_yaml["settings"]["api_id"]
api_hash = locales_yaml["settings"]["api_hash"]
api_key = locales_yaml["settings"]["api_key"]
bot_owners = locales_yaml["settings"]["bot_owners"]
mongo_database = locales_yaml["settings"]["database_url"]
enable_message_streaming = True
models = locales_yaml["settings"]["available_text_models"]
n_chat_modes_per_page = 6
info = locales_yaml["info"]

help_message = """
**Commands:**

◇ /retry : Regenerate last bot response
◇ /new : Start new chat box
◇ /mode : Select chat mode
◇ /help : Show help message
◇ /payment : Make payment 
◇ /balance : Show your balance  

✅ Generate images from text prompts in <b>👩‍🎨 Artist</b> `/mode` 
✅ Generate voice from text in 🎙 Speaker
"""

CRYPTO_API_URL = 'https://pay.crypt.bot/'
CRYPTO_API_KEY = ''
payment_token = ''