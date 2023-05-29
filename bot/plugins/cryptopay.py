import os
import config
from pyrogram import filters, enums
from requests import get
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton,CallbackQuery
from bot import app,user_tasks
from data.database import db

@app.on_callback_query(filters.regex("crypto"))
async def crypto_pay_menu(_, query:CallbackQuery):
    q_data = query.data.split()
    if len(q_data) == 1 :
        return await query.edit_message_text(
            "How many **tokens** do you want to buy?",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("💎 +500K Tokens - 4.99$", callback_data=f"crypto 500")
                        ],
                        [
                            InlineKeyboardButton("💎 +1M Tokens - 6.99$", callback_data=f"crypto 1")
                        ],
                        [
                            InlineKeyboardButton("💎 +2M Tokens - 9.99$", callback_data=f"crypto 2")
                        ],
                        [
                            InlineKeyboardButton("💎 +3M Tokens - 13.99$", callback_data=f"crypto 3"),
                        ],
                        [
                            InlineKeyboardButton("💎 +5M Tokens - 15.99$", callback_data=f"crypto 5"),
                        ]
                    ]))
    
    if len(q_data) == 2 :
        if q_data[1] == "500" : invoice_amount = 4.99
        if q_data[1] == "1" : invoice_amount = 6.99
        if q_data[1] == "2" : invoice_amount = 9.99
        if q_data[1] == "3" : invoice_amount = 13.99
        if q_data[1] == "5" : invoice_amount = 15.99
        await query.edit_message_text(
            f"Are you sure that you want to create a belowe payment.\n{invoice_amount} USDT",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Yes sure ✅", callback_data=f"crypto {q_data[1]} ok")],
                        [InlineKeyboardButton("🔙 Back", callback_data=f"crypto")]
                    ]))
        return
    
    if len(q_data) == 3:
        print(q_data[1])
        invoice_amount = ""
        label = ''
        if q_data[1] == "500" : 
            invoice_amount = 4.99
            label = '500K ChatGPT Tokens'
        if q_data[1] == "1" : 
            invoice_amount = 6.99
            label = '1M ChatGPT Tokens'
        if q_data[1] == "2" : 
            invoice_amount = 9.99
            label = '2M ChatGPT Tokens'
        if q_data[1] == "3" : 
            invoice_amount = 13.99
            label = '3M ChatGPT Tokens'
        if q_data[1] == "5" : 
            invoice_amount = 15.99
            label = '5M ChatGPT Tokens'

        invoicehead = {"asset":"USDT",
                       "amount":invoice_amount,
                       "description":label}
        
        cinvoce = get(f"{config.CRYPTO_API_URL}api/createInvoice", headers={"Crypto-Pay-API-Token":config.CRYPTO_API_KEY}, data=invoicehead).json()
        print(cinvoce)
        payment_url = cinvoce["result"]["pay_url"]
        invoice_id = int(cinvoce["result"]["invoice_id"])
        await query.edit_message_text("""
Open Crypto Bot by clicking **Pay now **.
Then do the payment.

Finally click **Check Payment **.
""",reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Pay now ↗️", url=payment_url)],
             [InlineKeyboardButton("Check Payment ", callback_data=f"check_crypt {invoice_id}")]]))

@app.on_callback_query(filters.regex("check_crypt"))
async def cryptoverify(_, query:CallbackQuery):
    q_data = query.data.split()
    if len(q_data) != 2: return
    invoice_id = int(q_data[1])
    checkpaid = get(f"{config.CRYPTO_API_URL}api/getInvoices", headers={"Crypto-Pay-API-Token":config.CRYPTO_API_KEY}, data={"invoice_ids":invoice_id}).json()
    if checkpaid["result"]["items"][0]["status"] != "paid" :
        await query.answer("You have't done your payment yet.", show_alert=True)
        return
    if checkpaid["result"]["items"][0]["status"] == "paid" :
        usdt_amount = checkpaid["result"]["items"][0]["amount"]
        await query.answer("Your payment was success.") 
        curent_credits = db.get_user_attribute(query.from_user.id, "user_balance")
        if usdt_amount == "500" : curent_credits += 500000 
        if usdt_amount == "1" : curent_credits += 1000000
        if usdt_amount == "2" : curent_credits += 2000000
        if usdt_amount == "3" : curent_credits += 3000000
        if usdt_amount == "5" : curent_credits += 5000000
        db.set_user_attribute(query.from_user.id, "user_balance", curent_credits)
        await query.edit_message_text(f"Successfully purchased credits ✅\nTotal Balance : {curent_credits}")