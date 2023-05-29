
import asyncio
from data.database import db
from bot import (
    user_semaphores,
    app
)

async def add_startup_user(message:str):
    user = message.from_user
    if not db.check_if_user_exists(user.id):
        db.add_new_user(
            int(user.id),
            days=3,
            username=user.username,
            first_name=user.first_name,
            last_name= user.last_name,
            )
        db.start_new_dialog(int(user.id))
    if user.id not in user_semaphores:
        user_semaphores[user.id] = asyncio.Semaphore(1)

async def is_answered(message):
    user_id = message.from_user.id
    if user_semaphores[user_id].locked():
        text = "👀 Please <b>wait</b> for a reply to the previous message\nOr you can /cancel it"
        await message.reply_text(text, reply_to_message_id=message.id)
        return True
    else:
        return False
    