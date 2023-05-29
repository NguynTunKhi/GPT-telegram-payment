import os
import config
from typing import Dict, List
import html
from uuid import uuid4
import config
from requests import get
from datetime import datetime
from bot import app,user_tasks
from data.database import db
from pyrogram import filters, enums
from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat, InlineQuery
from pyrogram.raw.types import InputMediaInvoice,DataJSON,Invoice,LabeledPrice,UpdateBotShippingQuery,ShippingOption,UpdateBotPrecheckoutQuery
from pyrogram.raw.functions.messages import SendMedia,SetBotPrecheckoutResults,SetBotShippingResults
from pyrogram import Client, ContinuePropagation
from pyrogram.types import Update, User, Chat
from pyrogram.raw.types import UpdateBotShippingQuery, UpdateBotPrecheckoutQuery
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton,CallbackQuery

_on_shipping_query_handlers: List[callable] = []
_on_checkout_query_handlers: List[callable] = []


def on_shipping_query(func: callable):
    _on_shipping_query_handlers.append(func)
    return func


def on_checkout_query(func: callable):
    _on_checkout_query_handlers.append(func)
    return func

@app.on_raw_update()
async def _raw(bot: Client, update: Update, users: Dict[int, User], chats: Dict[int, Chat]):
    if isinstance(update, UpdateBotShippingQuery):
        for handler in _on_shipping_query_handlers:
            await handler(bot, update, users, chats)
    elif isinstance(update, UpdateBotPrecheckoutQuery):
        for handler in _on_checkout_query_handlers:
            await handler(bot, update, users, chats)
    else:
        raise ContinuePropagation()
    
@app.on_callback_query(filters.regex("card"))
async def card_pay_menu(_, query:CallbackQuery):
    q_data = query.data.split()
    if len(q_data) == 1 :
        return await query.edit_message_text(
            "How many **tokens** do you want to buy?",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("💳 +500K Tokens - 4.99$", callback_data=f"card 500")
                        ],
                        [
                            InlineKeyboardButton("💳 +1M Tokens - 6.99$", callback_data=f"card 1")
                        ],
                        [
                            InlineKeyboardButton("💳 +2M Tokens - 9.99$", callback_data=f"card 2")
                        ],
                        [
                            InlineKeyboardButton("💳 +3M Tokens - 13.99$", callback_data=f"card 3"),
                        ],
                        [
                            InlineKeyboardButton("💳 +5M Tokens - 15.99$", callback_data=f"card 5"),
                        ]
                    ]))
    
    if len(q_data) == 2 :
        if q_data[1] == "500" : invoice_amount = 4.99
        if q_data[1] == "1" : invoice_amount = 6.99
        if q_data[1] == "2" : invoice_amount = 9.99
        if q_data[1] == "3" : invoice_amount = 13.99
        if q_data[1] == "5" : invoice_amount = 15.99
        await query.edit_message_text(
            f"Are you sure that you want to create a belowe payment.\n{invoice_amount} USD",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Yes sure ✅", callback_data=f"card {q_data[1]} ok")],
                        [InlineKeyboardButton("🔙 Back", callback_data=f"card")]
                    ]))
        return
    
    if len(q_data) == 3:
        print(q_data[1])
        invoice_amount = ""
        label = ''
        if q_data[1] == "500" : 
            invoice_amount = 499
            label = '500K ChatGPT Tokens'
        if q_data[1] == "1" : 
            invoice_amount = 699
            label = '1M ChatGPT Tokens'
        if q_data[1] == "2" : 
            invoice_amount = 999
            label = '2M ChatGPT Tokens'
        if q_data[1] == "3" : 
            invoice_amount = 1399
            label = '3M ChatGPT Tokens'
        if q_data[1] == "5" : 
            invoice_amount = 1599
            label = '5M ChatGPT Tokens'

        prices = [LabeledPrice(amount=invoice_amount, label=label)]
        invoice = Invoice(
            currency="USD",
            prices=prices,
            test=True)

        await app.invoke(
        SendMedia(
            peer=await app.resolve_peer(query.message.chat.id),
            media=InputMediaInvoice(
                title=label,
                description="Tap the button below and pay",
                invoice=invoice,
                payload=f"{query.from_user.id}_bought".encode(),
                provider=config.payment_token,
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),
            message="",
            random_id=app.rnd_id(),
        ))

@on_checkout_query
async def process_checkout_query(
    bot: Client,
    query: UpdateBotPrecheckoutQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    curent_credits = db.get_user_attribute(query.user_id, "user_balance")
    usdt_amount = query.total_amount
    print(usdt_amount)

    if usdt_amount == 499 : curent_credits += 500000 
    if usdt_amount == 699 : curent_credits += 1000000
    if usdt_amount == 999 : curent_credits += 2000000
    if usdt_amount == 1399 : curent_credits += 3000000
    if usdt_amount == 1599 : curent_credits += 5000000

    db.set_user_attribute(query.user_id, "user_balance", curent_credits)
    await app.send_message(query.user_id,f"Successfully purchased credits ✅\nTotal Balance : {curent_credits}")
    return await bot.invoke(
        SetBotPrecheckoutResults(query_id=query.query_id,success=True,error=None))
