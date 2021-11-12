# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from pyrogram import filters
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot
from pyrogram.types.messages_and_media import message
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests

API_S= Var.API_SB
BASE_URL="https://api.streamsb.com/api/upload/url?key="+API_S+"&url="
STREAMSB_URL="https://embedsb.com/"
DROP_URL="https://droplink.co/api?api=d61f38da5372ed4c13655f94ee3564b20f6fd525&url="

def detect_type(m: Message):
    if m.document:
        return m.document
    elif m.video:
        return m.video
    elif m.audio:
        return m.audio
    else:
        return
    

@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def media_receive_handler(_, m: Message):
    file = detect_type(m)
    file_name = ''
    if file:
        file_name = file.file_name
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

    stream_link = Var.URL  + str(log_msg.message_id) + '/' +quote_plus(file_name) if file_name else ''
    response= requests.get(BASE_URL+stream_link)  
    final_sb_url =STREAMSB_URL+response.json().get("result").get("filecode")+".html" 
    response2= requests.get(DROP_URL+final_sb_url+"&alias="+file_name)
    final_drop_url=response2.json().get("shortenedUrl")
    await m.reply_text(
        text="`{}`".format(final_drop_url),
        quote=True,
        
    )
