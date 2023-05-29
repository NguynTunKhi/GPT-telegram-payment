#First pyrogram ChatGPT bot in telegram
#copyright - 2023 ~ Supun Maduranga

#Credits 
#01.Openai
#02.https://github.com/karfly/chatgpt_telegram_bot

#pricing plan

#50 token per response
#100 token per image 
#150 token per voice search

import config
from pyrogram import Client

user_semaphores = {}
user_tasks = {}
command_list = ["/balance","/payment","/start","/new","/mode","/img","/settings","/","/retry","/help","/balance","/cancel","/balance"]
plugins = dict(root="bot/plugins")

app = Client(
    "Telegram_Ai",
    api_id = config.api_id,
    api_hash = config.api_hash,
    bot_token = config.bot_token,
    plugins = plugins)


